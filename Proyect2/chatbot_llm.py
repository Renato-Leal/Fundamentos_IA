"""
Chatbot de juegos de mesa con LLM.
Uso (Gemini, plan gratuito):
    pip install google-genai
    export GEMINI_API_KEY="tu_clave"         # (Windows: set GEMINI_API_KEY=...)
La clave se crea gratis en https://aistudio.google.com (Get API key).
"""
import json
import os
import re
import sys
import time
from dotenv import load_dotenv
load_dotenv()

# Modelo con plan gratuito. Si Google lo retira, cambia el nombre aquí
# o define la variable de entorno MODELO_LLM.
MODELO = os.environ.get("MODELO_LLM", "gemini-3.1-flash-lite")
# Si el modelo principal está saturado o falla, se prueba este
MODELO_RESPALDO = os.environ.get("MODELO_RESPALDO", "gemini-3.8-flash")
ARCHIVO_PL = os.path.join(os.path.dirname(__file__), "juegos_de_mesa.pl")

# Predicados con un solo valor y predicados con varios valores por juego
UNICOS = ["min_jugadores", "max_jugadores", "dificultad", "requiere_tablero",
          "tiempo_cronometrado", "duracion_minutos", "edad_minima",
          "tiene_expansion"]
MULTIPLES = ["categoria", "idioma"]


#  1. Leer los hechos del archivo .pl 
def cargar_hechos(ruta=ARCHIVO_PL):
    """Convierte los hechos Prolog en un diccionario {id_juego: {campo: valor}}."""
    juegos = {}
    patron = re.compile(r"^(\w+)\((.*)\)\.$")
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.split("%")[0].strip()       # quitar comentarios
            m = patron.match(linea)
            if not m:
                continue
            pred, args = m.group(1), m.group(2)
            partes = [a.strip().strip("'") for a in args.split(",", 1)]
            if len(partes) != 2:
                continue
            id_juego, valor = partes
            if pred == "juego":
                juegos.setdefault(id_juego, {})["nombre"] = valor
            elif pred in UNICOS:
                juegos.setdefault(id_juego, {})[pred] = (
                    int(valor) if valor.isdigit() else valor)
            elif pred in MULTIPLES:
                juegos.setdefault(id_juego, {}).setdefault(pred, []).append(valor)
    return juegos


#  2. Prompt de sistema 
def construir_prompt(juegos):
    datos = json.dumps(juegos, ensure_ascii=False, separators=(",", ":"))
    return f"""Eres un asistente experto en especificaciones técnicas de juegos de mesa
y recomiendas juegos según el grupo del usuario.

REGLAS:
1. Responde SOLO usando la base de datos de abajo. Si un dato o juego no está,
   dilo claramente; no inventes.
2. Un juego NO es válido si jugadores < min_jugadores o jugadores > max_jugadores.
3. Un juego NO es válido si la edad del jugador más joven < edad_minima.
4. Si el usuario no da número de jugadores o edades y los necesitas, pregúntalos.
5. Al descartar un juego, explica el motivo (faltan jugadores, sobran, edad).
6. Responde en español neutro, breve y claro.

BASE DE DATOS (JSON):
{datos}
"""


#  3. Llamada al LLM (único punto que depende del proveedor) 
def llamar_llm(system, historial):
    from google import genai
    from google.genai import types

    cliente = genai.Client()                          # lee GEMINI_API_KEY
    # Gemini usa el rol "model" en vez de "assistant"
    contenido = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in historial
    ]
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=2000,                       # los tokens de "pensar" también cuentan aquí
        thinking_config=types.ThinkingConfig(thinking_level="low"),  # razonamiento mínimo: más rápido
    )
    # Errores temporales: 429 (límite del plan gratuito) y 503 (Google saturado).
    # Se reintenta con pausas y, si no resulta, se prueba el modelo de respaldo.
    ultimo_error = None
    for modelo in dict.fromkeys([MODELO, MODELO_RESPALDO]):   # sin repetir
        for intento in range(3):
            try:
                resp = cliente.models.generate_content(
                    model=modelo, contents=contenido, config=config)
                return resp.text
            except Exception as e:
                ultimo_error = e
                temporal = any(c in str(e) for c in
                               ("429", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))
                if temporal and intento < 2:
                    espera = 5 * (intento + 1)
                    print(f"  (Google ocupado con {modelo}, reintentando en {espera} s...)")
                    time.sleep(espera)
                    continue
                print(f"  (no se pudo con {modelo}, probando alternativa...)")
                break
    raise ultimo_error


#  4. Función que usará la interfaz web 
_JUEGOS = cargar_hechos()
_SYSTEM = construir_prompt(_JUEGOS)


def responder(pregunta, historial=None):
    """Responde una pregunta. 'historial' es una lista de mensajes previos
    ({'role': ..., 'content': ...}) para mantener la conversación."""
    mensajes = list(historial or []) + [{"role": "user", "content": pregunta}]
    return llamar_llm(_SYSTEM, mensajes)


#  5. Modos de ejecución 
def conversar():
    print("Chatbot de juegos de mesa (escribe 'salir' para terminar)")
    historial = []
    while True:
        pregunta = input("Tú: ").strip()
        if pregunta.lower() in ("salir", "exit"):
            break
        t0 = time.time()
        try:
            respuesta = responder(pregunta, historial)
        except Exception as e:
            print("Bot: No pude obtener respuesta ahora. Intenta de nuevo en un momento.")
            print(f"  (detalle: {str(e)[:150]})\n")
            continue
        segundos = time.time() - t0
        historial += [{"role": "user", "content": pregunta},
                      {"role": "assistant", "content": respuesta}]
        print("Bot:", respuesta, "\n")


def evaluar(archivo_preguntas, archivo_salida):
    """Lee una pregunta por línea y guarda las respuestas para el informe."""
    with open(archivo_preguntas, encoding="utf-8") as f:
        preguntas = [l.strip() for l in f if l.strip()]
    resultados = []
    for i, p in enumerate(preguntas, 1):
        t0 = time.time()
        try:
            r = responder(p)                          # sin historial: cada pregunta es independiente
        except Exception as e:
            r = f"ERROR: {str(e)[:150]}"              # queda registrado y se sigue con la siguiente
        segundos = round(time.time() - t0, 1)
        time.sleep(4)                                 # pausa para no pasar el límite gratuito
        resultados.append({"n": i, "pregunta": p, "respuesta": r, "segundos": segundos})
        print(f"[{i}/{len(preguntas)}] {p}\n  -> {r}\n")
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print("Guardado en", archivo_salida)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "evaluar":
        evaluar(sys.argv[2], sys.argv[3])
    else:
        conversar()
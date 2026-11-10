"""El LLM solo traduce; Prolog razona.
Uso: python chatbot.py   |   python chatbot.py evaluar preguntas.txt salida.json
Incluir en el .env:   SWIPL=C:\Program Files\swipl\bin\swipl.exe (dirección de donde está prolog)
"""
import json
import os
import re
import subprocess
import sys
import time

from dotenv import load_dotenv
load_dotenv()

MODELO = os.environ.get("MODELO_LLM", "gemini-3.1-flash-lite")
MODELO_RESPALDO = os.environ.get("MODELO_RESPALDO", "gemini-3.8-flash")
SWIPL = os.environ.get("SWIPL", "swipl")
PL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "juegos_de_mesa.pl")
ATRIBUTOS = ["min_jugadores", "max_jugadores", "dificultad", "categoria", "requiere_tablero",
             "tiempo_cronometrado", "duracion_minutos", "edad_minima", "tiene_expansion", "idioma"]
ULTIMA = {}


def cargar_juegos():
    """Lee del .pl solo los id y nombres de los juegos."""
    juegos = {}
    with open(PL, encoding="utf-8") as f:
        for linea in f:
            m = re.match(r"^juego\((\w+),\s*'(.*)'\)\.", linea)
            if m:
                juegos[m.group(1)] = m.group(2)
    return juegos


JUEGOS = cargar_juegos()

PROMPT_TRADUCTOR = """Traduce la pregunta del usuario a un JSON. NO respondas la pregunta ni uses conocimiento propio.
Responde SOLO el JSON.

Juegos (usa el id; si el juego no está en la lista, usa "desconocido"):
""" + "\n".join(f"- {i}: {n}" for i, n in JUEGOS.items()) + """

Formatos:
{"intent":"puede_jugar","juego":<id o null>,"jugadores":<número>,"edad":<edad del menor o null>}
{"intent":"dato","juego":<id>,"atributo":<uno de: """ + ", ".join(ATRIBUTOS) + """>}
{"intent":"recomendar","jugadores":<número>,"edad":<número o null>,"categoria":<ej: estrategia, casual, rol, cartas>}
{"intent":"fuera_de_dominio"}

Ejemplos:
"¿Podemos jugar Catán 2 personas?" -> {"intent":"puede_jugar","juego":"catan","jugadores":2,"edad":null}
"Somos 4 y el menor tiene 9, ¿qué podemos jugar?" -> {"intent":"puede_jugar","juego":null,"jugadores":4,"edad":9}
"¿Cuántos jugadores admite UNO como máximo?" -> {"intent":"dato","juego":"uno","atributo":"max_jugadores"}
"""

PROMPT_REDACTOR = """Redacta en español, breve y claro, la respuesta a la pregunta usando SOLO el RESULTADO.
No agregues datos ni apliques reglas.
"si" = se puede jugar. "no(motivos)" = no se puede, explica los motivos. "[a,b]" = lista; "[]" = ninguno cumple."""


def llamar_llm(system, historial):
    from google import genai
    from google.genai import types

    cliente = genai.Client()
    contenido = [types.Content(role="model" if m["role"] == "assistant" else "user",
                               parts=[types.Part(text=m["content"])]) for m in historial]
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=2000,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    )
    error = None
    for modelo in dict.fromkeys([MODELO, MODELO_RESPALDO]):
        for intento in range(3):
            try:
                return cliente.models.generate_content(
                    model=modelo, contents=contenido, config=config).text
            except Exception as e:
                error = e
                if intento < 2 and any(c in str(e) for c in ("429", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                    time.sleep(5 * (intento + 1))
                    continue
                break
    raise error


def objetivo(c):
    """Convierte el JSON del LLM en una consulta Prolog (solo consultas permitidas)."""
    juego = c.get("juego")
    if juego and juego not in JUEGOS:
        return None
    if c.get("intent") == "dato" and c.get("atributo") in ATRIBUTOS and juego:
        return f"findall(V,{c['atributo']}({juego},V),L),write(L)"
    if not str(c.get("jugadores") or "").isdigit():
        return None
    n = int(c["jugadores"])
    e = int(c["edad"]) if str(c.get("edad") or "").isdigit() else 99
    if c.get("intent") == "puede_jugar":
        if juego:
            return (f"(puede_jugar({juego},{n},{e})->R=si;"
                    f"findall(M,motivo_rechazo({juego},{n},{e},M),Ms),R=no(Ms)),write(R)")
        return f"findall(N,(puede_jugar(J,{n},{e}),juego(J,N)),L),write(L)"
    if c.get("intent") == "recomendar" and re.fullmatch(r"[a-z_]+", str(c.get("categoria"))):
        return f"findall(N,(recomendar(J,{n},{e},{c['categoria']}),juego(J,N)),L),write(L)"
    return None


def prolog(meta):
    cmd = [SWIPL, "-q", "-s", PL, "-g", "set_stream(user_output,encoding(utf8))," + meta, "-t", "halt"]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def responder(pregunta, historial=None):
    texto = llamar_llm(PROMPT_TRADUCTOR, (historial or []) + [{"role": "user", "content": pregunta}])
    m = re.search(r"\{.*\}", texto or "", re.S)
    try:
        c = json.loads(m.group(0))
    except (AttributeError, json.JSONDecodeError):
        c = {}
    ULTIMA.clear()
    ULTIMA["consulta"] = c
    if c.get("intent") == "fuera_de_dominio":
        return "Solo puedo responder sobre juegos de mesa."
    meta = objetivo(c)
    if not meta:
        return "No te entendí o no tengo ese juego. Indícame el juego, cuántos son y sus edades."
    resultado = prolog(meta)
    if c.get("intent") != "dato" and not str(c.get("edad") or "").isdigit():
        resultado += " (edad no indicada: no se verificó la edad mínima)"
    ULTIMA.update(objetivo=meta, resultado=resultado)
    return llamar_llm(PROMPT_REDACTOR, [{"role": "user", "content": f"Pregunta: {pregunta}\nRESULTADO: {resultado}"}])


def conversar():
    historial = []
    while True:
        pregunta = input("Tú: ").strip()
        if pregunta.lower() in ("salir", "exit"):
            break
        try:
            respuesta = responder(pregunta, historial)
        except Exception as e:
            print(f"Bot: Error, intenta de nuevo. ({str(e)[:150]})\n")
            continue
        historial += [{"role": "user", "content": pregunta}, {"role": "assistant", "content": respuesta}]
        print("Bot:", respuesta, "\n")


def evaluar(archivo_preguntas, archivo_salida):
    with open(archivo_preguntas, encoding="utf-8") as f:
        preguntas = [l.strip() for l in f if l.strip()]
    resultados = []
    for i, p in enumerate(preguntas, 1):
        t0 = time.time()
        try:
            r = responder(p)
        except Exception as e:
            r = f"ERROR: {str(e)[:150]}"
        resultados.append({"n": i, "pregunta": p, "respuesta": r,
                           "segundos": round(time.time() - t0, 1), **ULTIMA})
        print(f"[{i}/{len(preguntas)}] {p}\n  -> {r}\n")
        time.sleep(4)
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "evaluar":
        evaluar(sys.argv[2], sys.argv[3])
    else:
        conversar()

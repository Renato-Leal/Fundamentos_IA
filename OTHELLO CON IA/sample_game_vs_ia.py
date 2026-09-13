"""Partida de Othello (Reversi): jugador humano (A) contra el agente (B)"""

from othello import OthelloBoard

# El usuario elige el tamaño del tablero (debe ser par y >= OthelloBoard.TAM_MIN)
board = None
while board is None:
    entrada = input(f"Ingrese el tamaño del tablero (par, mínimo {OthelloBoard.TAM_MIN}): ")
    try:
        n = int(entrada)
        board = OthelloBoard(n, player1="A", player2="B")
    except ValueError as e:
        print(f"Tamaño inválido: {e}")

# Profundidad de búsqueda del agente (a mayor profundidad, "piensa" más,
# pero también demora más en decidir su jugada)
profundidad = None
while profundidad is None:
    entrada = input("Ingrese la profundidad de búsqueda del agente (ej: 3): ")
    try:
        profundidad = int(entrada)
        if profundidad < 1:
            raise ValueError("La profundidad debe ser al menos 1.")
    except ValueError as e:
        print(f"Valor inválido: {e}")
        profundidad = None

HUMANO = 1  # jugador A, hace la primera jugada
AGENTE = 2  # jugador B, el agente con Minimax + poda Alfa-Beta

turn = HUMANO
print(board)

while not board.is_game_over():
    jugadas_legales = board.get_legal_moves(turn)

    if not jugadas_legales:
        # Paso obligatorio: no hay jugadas legales para este jugador
        print(f"Jugador {turn} ({board.player_symbol(turn)}) no tiene jugadas legales, pasa turno.")
        turn = AGENTE if turn == HUMANO else HUMANO
        continue

    if turn == AGENTE:
        # Le toca al agente: decide su jugada con Minimax + poda Alfa-Beta
        print("El agente está pensando...")
        r, c = board.mejor_movimiento(AGENTE, profundidad)
        board.play2(r, c)
        print(f"El agente ({board.player_symbol(AGENTE)}) juega en ({r}, {board.column_label(c)})")
        print(board)
        turn = HUMANO
        continue

    # Le toca al humano: mostramos sus jugadas legales (con letra) y pedimos jugada
    jugadas_letra = [(r, board.column_label(c)) for r, c in jugadas_legales]
    jugadas_texto = ", ".join(f"({r}, {c})" for r, c in jugadas_letra)
    print(f"Jugadas legales para jugador {turn} ({board.player_symbol(turn)}): [{jugadas_texto}]")

    jugada_valida = False
    while not jugada_valida:
        # El jugador debe ingresar "fila, columna" (ej: "1, C")
        entrada = input(f"Ingrese jugada de jugador {turn} ({board.player_symbol(turn)}): ")
        try:
            fila_texto, columna_texto = entrada.split(',')
            r = int(fila_texto.strip())
            c = OthelloBoard.column_number(columna_texto)
            jugada_valida = board.play1(r, c)
        except ValueError:
            print("Formato inválido. Use: fila, columna (ej: 1, C)")
            continue
        except LookupError:
            print("Esa coordenada no existe en el tablero.")
            continue

        if not jugada_valida:
            print("Jugada inválida, intente de nuevo.")

    print(board)
    turn = AGENTE

# Fin de la partida: se cuentan las fichas y se determina el ganador
print("¡Partida terminada!")
print(board.contar_fichas())

"""Este es un ejemplo de implementación de una partida de Othello (Reversi)
para dos jugadores"""

from Othello import OthelloBoard

# El usuario elige el tamaño del tablero (debe ser par y >= OthelloBoard.TAM_MIN)
board = None
while board is None:
    entrada = input(f"Ingrese el tamaño del tablero (par, mínimo {OthelloBoard.TAM_MIN}): ")
    try:
        n = int(entrada)
        board = OthelloBoard(n, player1="O", player2="X")
    except ValueError as e:
        print(f"Tamaño inválido: {e}")
 
turn = 1  # 1 = jugador 1 (O), 2 = jugador 2 (X)
pases_seguidos = 0
 
print(board)

while not board.is_game_over():
    jugadas_legales = board.get_legal_moves(turn)   # ← turn, no piece

    if not jugadas_legales:
        print(f"Jugador {turn} ({board.player_symbol(turn)}) no tiene jugadas legales, pasa turno.")
        pases_seguidos += 1
        turn = 2 if turn == 1 else 1
        continue

    print(f"Jugadas legales para jugador {turn} ({board.player_symbol(turn)}): {jugadas_legales}")

    jugada_valida = False
    while not jugada_valida:
        entrada = input(f"Ingrese jugada de jugador {turn} ({board.player_symbol(turn)}): ")
        try:
            r, c = map(int, entrada.split(','))
        except ValueError:
            print("Formato inválido. Use: fila, columna (ej: 1, 3)")
            continue

        if turn == 1:
            jugada_valida = board.play1(r, c)
        else:
            jugada_valida = board.play2(r, c)

        if not jugada_valida:
            print("Jugada inválida, intente de nuevo.")

    pases_seguidos = 0
    print(board)
    turn = 2 if turn == 1 else 1

# Fin de la partida: se cuentan las fichas y se determina el ganador
print("¡Partida terminada!")
print(board.contar_fichas())
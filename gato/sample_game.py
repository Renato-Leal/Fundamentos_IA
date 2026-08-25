"""Este es un ejemplo de implementación cuma de un juego de gato para
dos jugadores"""

from tictactoe import TicTacToeBoard

winner = ""

# Ejemplo de construcción
board = TicTacToeBoard(player1="X", player2="O")

turn = 1
# El gato no tiene más de nueve turnos
while winner == "" and turn <= 9:
    # "X" es el jugador 1 y "O" es el jugador 2, porque sí
    player = "X" if turn % 2 == 1 else "O"
    # Voy a confiar en el usuario, algo que nunca se hace :v
    # El jugador debe ingresar "fila, columna"
    coords = map(int, input(f"Ingrese jugada de jugador {player}: ").split(','))
    if turn % 2 == 0:
        # Las coordenadas son una tupla, pero la función acepta valores por separado
        # Se puede hacer que acepte las dos cosas, como __getitem__ de board.Board
        board.play2(*coords)
    else:
        board.play1(*coords)

    # Valida si ganó el jugador actual
    print(1 if turn % 2 == 1 else 2)
    print(board.validate_winner(1 if turn % 2 == 1 else 2))
    print(winner)
    if board.validate_winner(1 if turn % 2 == 1 else 2):
        winner = player
    
    # Muestra tablero y avanza el turno
    print(board)
    turn += 1

# Muestra el ganador
if winner:
    print(f"¡Gana el jugador {winner}! Omedetou 👏 (?)")
else:
    print("Empate D:")

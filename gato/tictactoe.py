from board import Board


class TicTacToeBoard(Board):
    """Tablero para jugar al gato/tres en línea/tres en raya, como le digan
    
    Esta clase extiende (hereda de) la clase base del tablero, para poder jugar
    específicamente al gato.
    """
    __player1: str  # ícono del jugador 1
    __player2: str  # ícono del jugador 2
    
    def __init__(self, player1: str = "O", player2: str = "X"):
        """Construye el tablero"""
        # El gato siempre es  de 3x3
        super().__init__(3)
        self.__player1 = player1
        self.__player2 = player2

    # En estas funciones, r = row (fila); c = column (columna)
    def play1(self, r: int, c: int) -> bool:
        """Jugada del jugador 1
        
        Retorna
        -------
        bool :
            True si la jugada se pudo hacer y es válida
        """
        if self.valid_move(r, c):
            self[r, c] = self.__player1
            return True
        else:
            return False

    def play2(self, r:int, c:int):
        """Jugada del jugador 2"""
        if self.valid_move(r, c):
            self[r, c] = self.__player2
            return True
        else:
            return False

    def validate_winner(self, player: int) -> bool:
        """Esta función valida si el jugador ganó"""
        if player == 1:
            check = self.__player1
        elif player == 2:
            check = self.__player2
        else:
            raise ValueError(f"Invalid player number: {player}")
    
        # Acá van las condiciones de victoria
        # Filas
        for i in range(1, 4):
            # Brujería de esta lógica: suma 1 por cada columna que tenga la marca
            # de este jugador
            row_marks = sum(1 for j in range(1, 4) if self[i, j] == check)
            if row_marks == 3:
                return True
        # Columnas
        for j in range(1, 4):
            # Brujería de esta lógica: suma 1 por cada columna que tenga la marca
            # de este jugador
            col_marks = sum(1 for i in range(1, 4) if self[i, j] == check)
            if col_marks == 3:
                return True
        
        # Diagonales
        main_diag = sum(1 for i in range(1, 4) if self[i, i] == check)
        # Diagonal secundaria
        sec_diag = sum(1 for i in range(1, 4) if self[i, 4 - i] == check)

        # Cualquiera de las dos que sea verdadera es victoria
        return main_diag == 3 or sec_diag == 3


# Para probar el módulo
if __name__ == "__main__":
    t = TicTacToeBoard()
    print(t)
    t.play1(3, 1)
    t.play2(2, 3)
    t.play1(2, 2)
    t.play2(3, 3)
    t.play1(1, 3)
    print(t)
    print(t.validate_winner(1))
    print(t.validate_winner(2))

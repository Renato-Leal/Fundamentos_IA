from board import Board


class OthelloBoard(Board):
    """Tablero para jugar Othello/Reversi

    Esta clase extiende (hereda de) la clase base del tablero, 
    """
    TAM_MIN = 4  # Tamaño mínimo permitido del tablero

    __player1: str  # ícono del jugador 1
    __player2: str  # ícono del jugador 2

    def __init__(self, size, player1: str = "A", player2: str = "B"):
        if not isinstance(size, int):
            raise ValueError("El tamaño debe ser un número entero.")
        if size % 2 != 0:
            raise ValueError("El tamaño debe ser un número par.")
        if size < self.TAM_MIN:
            raise ValueError(f"El tamaño mínimo es {self.TAM_MIN}x{self.TAM_MIN}.")

        super().__init__(size)
        self.__player1 = player1
        self.__player2 = player2
        self.__setup_initial()

    def __setup_initial(self):
        """Coloca las 4 fichas iniciales según m = n // 2"""
        m = self.size // 2
        self[m, m] = self.__player1
        self[m + 1, m + 1] = self.__player1
        self[m, m + 1] = self.__player2
        self[m + 1, m] = self.__player2

    def player_symbol(self, player: int) -> str:
        """Traduce el número de jugador (1 o 2) a su símbolo en el tablero

        Método público: lo necesita, por ejemplo, sample_game.py para
        mostrarle al usuario con qué ficha está jugando cada turno
        """
        return self.__symbol(player)

    def __symbol(self, player: int) -> str:
        """Traduce el número del jugador (1 o 2) a su ficha correspondiente"""
        if player == 1:
            return self.__player1
        elif player == 2:
            return self.__player2
        else:
            raise ValueError(f"Invalid player number: {player}")

    def __opponent(self, player: int) -> int:
        """Retorna el número del jugador contrario"""
        if player == 1:
            return 2
        elif player == 2:
            return 1
        else:
            raise ValueError(f"Invalid player number: {player}")

    def get_flips(self, r: int, c: int, player: int) -> list[tuple[int, int]]:
        """Busca, en las 8 direcciones, qué fichas rivales quedarían
        encerradas (y se voltearían) si 'player' juega en (r, c)

        Retorna
        -------
        list[tuple[int, int]] :
            Coordenadas de todas las fichas que se voltearían. Si la lista
            está vacía, significa que la jugada no encierra nada (inválida)
        """
        own = self.__symbol(player)
        opp = self.__symbol(self.__opponent(player))
        flips: list[tuple[int, int]] = []

        for dr, dc in Board.DIRECTIONS:
            path: list[tuple[int, int]] = []
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc) and self[nr, nc] == opp:
                path.append((nr, nc))
                nr += dr
                nc += dc
            if path and self.in_bounds(nr, nc) and self[nr, nc] == own:
                flips.extend(path)

        return flips

    def is_legal_move(self, r: int, c: int, player: int) -> bool:
        """Valida si 'player' puede jugar legalmente en (r, c)"""
        if not self.valid_move(r, c):
            return False
        return len(self.get_flips(r, c, player)) > 0

    def __execute_move(self, r: int, c: int, player: int) -> bool:
        """Coloca la ficha de 'player' en (r, c) y voltea lo que corresponda"""
        if not self.is_legal_move(r, c, player):
            return False
        symbol = self.__symbol(player)
        self[r, c] = symbol
        for fr, fc in self.get_flips(r, c, player):
            self[fr, fc] = symbol
        return True

    def play1(self, r: int, c: int) -> bool:
        """Jugada del jugador 1

        Retorna
        -------
        bool :
            True si la jugada se pudo hacer y es válida
        """
        return self.__execute_move(r, c, 1)

    def play2(self, r: int, c: int) -> bool:
        """Jugada del jugador 2"""
        return self.__execute_move(r, c, 2)

    def get_legal_moves(self, player: int) -> list[tuple[int, int]]:
        """Retorna todas las casillas donde 'player' tiene una jugada legal

        """
        n = self.size
        return [
            (r, c)
            for r in range(1, n + 1)
            for c in range(1, n + 1)
            if self.is_legal_move(r, c, player)
        ]

    def is_full(self) -> bool:
        """Retorna True si no quedan casillas vacías en el tablero"""
        n = self.size
        return all(
            self[r, c] != Board.EMPTY_SPACE
            for r in range(1, n + 1)
            for c in range(1, n + 1)
        )

    def is_game_over(self) -> bool:
        """Retorna True si la partida terminó"""
        if self.is_full():
            return True
        return len(self.get_legal_moves(1)) == 0 and len(self.get_legal_moves(2)) == 0

    def contar_fichas(self):
        """Cuenta cuántas fichas hay en el tablero de cada color"""
        n = self.size
        B_ficha = sum(
            1 for i in range(1, n + 1) for j in range(1, n + 1)
            if self[i, j] == self.__player1
        )
        A_ficha = sum(
            1 for i in range(1, n + 1) for j in range(1, n + 1)
            if self[i, j] == self.__player2
        )
        marcador = f"Fichas B :{B_ficha} || Fichas A :{A_ficha}"
        if B_ficha > A_ficha:
            return f"{marcador} || Gana el jugador 1"
        elif A_ficha > B_ficha:
            return f"{marcador} || Gana el jugador 2"
        else:
            return f"{marcador} || Empate"
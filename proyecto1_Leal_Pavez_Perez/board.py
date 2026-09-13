import math

class Board:
    __places: list[list[str]]  # Tablero en sí
    __size: int  # Tamaño del tablero

    EMPTY_SPACE = "."  # Constante de clase que marca los espacios vacíos

    # Las 8 direcciones posibles a partir de una casilla: (delta_fila, delta_columna)
    # Sirven para recorrer el tablero en línea recta (arriba, abajo, izq, der y diagonales)
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    def __init__(self, n: int = 3):
        """Crea un tablero"""
        # Define la lista para almacenar las posiciones
        self.__places = [
            [Board.EMPTY_SPACE] * n for _ in range(n)
        ]
        self.__size = n

    @property
    def size(self) -> int:
        """Tamaño del tablero (n), expuesto públicamente para las clases hijas"""
        return self.__size

    @staticmethod
    def __column_label(index: int) -> str:
        letter = chr(ord('A') + index % 26)   # letra dentro del ciclo actual (0-25)
        cycle = index // 26                    # cuántas "vueltas" completas al alfabeto
        return letter if cycle == 0 else f"{letter}{cycle}"

    def column_label(self, column: int) -> str:
        """Traduce un número de columna (1-indexado) a su letra"""
        return self.__column_label(column - 1)
    
    @staticmethod
    def column_number(label: str) -> int:
        """Traduce una etiqueta de columna (A, B, ..., Z, A1, B1, ...)
        a su número de columna (1-indexado, el mismo formato que usa
        self[r, c])
 
        Es el método inverso de __column_label. Público, para que
        sample_game.py pueda usarlo al leer la jugada del usuario.
        """
        label = label.strip().upper()
        if not label or not label[0].isalpha():
            raise ValueError(f"Columna inválida: {label}")
        letter = label[0]
        cycle_str = label[1:]
        if cycle_str and not cycle_str.isdigit():
            raise ValueError(f"Columna inválida: {label}")
        cycle = int(cycle_str) if cycle_str else 0
        index = cycle * 26 + (ord(letter) - ord('A'))
        return index + 1

    def __str__(self) -> str:
        """Función que es llamada cuando se hace str(self)"""
        col_labels = [self.__column_label(i) for i in range(self.__size)]
        row_labels = [str(i) for i in range(1, self.__size + 1)]
        width = max(len(label) for label in col_labels + row_labels)
 
        header = " " * width + " "
        header += " ".join(f"{label:>{width}}" for label in col_labels)
        board = header + "\n"
        for row_label, line in zip(row_labels, self.__places):
            cells = " ".join(f"{cell:>{width}}" for cell in line)
            board += f"{row_label:>{width}} {cells}\n"
        return board

    def __repr__(self) -> str:
        """Función para cuando se llama repr(self)"""
        return f"Board({self.__size})"

    def __len__(self) -> int:
        """Función para cuando se llama len(self)"""
        return self.__size

    def __check_valid_range(self, r: int) -> bool:
        """Valida que el valor esté dentro del rango del tablero

        Esto considera que las posiciones van de 1 a n
        """
        # Nombre con dos guiones bajos al inicio se interpreta como privada
        if 1 > r or r > self.__size:
            return False
        return True

    def in_bounds(self, r: int, c: int) -> bool:
        """Valida que la coordenada (r, c) esté dentro del tablero

        A diferencia de __check_valid_range, revisa fila y columna juntas
        de una vez, y es público para que las clases hijas (u otro código)
        puedan usarlo al recorrer el tablero, por ejemplo con Board.DIRECTIONS
        """
        return self.__check_valid_range(r) and self.__check_valid_range(c)

    def __getitem__(self, subscript: int | tuple):
        """Implementa self[subscript]

        En este caso, `subscript` puede ser un entero (fila) o una tupla
        (coordenadas).

        Levanta excepciones, si no se usa bien.
        """
        if isinstance(subscript, tuple):
            # Si es una tupla
            # Si son más o menos que filas y columnas
            if len(subscript) != 2:
                raise ValueError("Coordenadas con más de 2 dimensiones")
            # Si la fila está fuera de rangoo
            if not self.__check_valid_range(subscript[0]):
                raise LookupError(f"Fila fuera de rango: {subscript[0]}")
            # Si la columna está fuera de rango
            if not self.__check_valid_range(subscript[1]):
                raise LookupError(f"Columna fuera de rango: {subscript[1]}")
            return self.__places[subscript[0] - 1][subscript[1] - 1]
        elif isinstance(subscript, int):
            # Si es un entero
            if not self.__check_valid_range(subscript):
                raise LookupError(f"Fila fuera de rango: {subscript}")
            return self.__places[subscript - 1]
        else:
            # Si el índice no es del tipo correcto
            raise TypeError("Dato inválido, ingrese dato en coordenada")

    def __setitem__(self, key: tuple, value: str) -> None:
        """Implementa self[key] = value

        El "índice" `key` tiene que ser un par de coordenadas
        """
        if not isinstance(key, tuple):
            raise TypeError(f"Subscript debe ser coordenadas (tuple), not {type(key)}")
        if len(key) != 2:
            raise ValueError("Coordenadas con más de 2 dimensiones")
        # Si la fila está fuera de rangoo
        if not self.__check_valid_range(key[0]):
            raise LookupError(f"Fila fuera de rango: {key[0]}")
        # Si la columna está fuera de rango
        if not self.__check_valid_range(key[1]):
            raise LookupError(f"Columna fuera de rango: {key[1]}")
        self.__places[key[0] - 1][key[1] - 1] = value

    def valid_move(self, r: int, c: int):
        """Valida que sea un movimiento válido, es decir, a una casilla libre

        Este método debería ser sobrecargado por un tablero hijo que
        permite movimientos válidos con otras reglas
        """
        return self[r, c] == Board.EMPTY_SPACE


   
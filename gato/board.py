import math


class Board:
    __places: list[list[str]]  # Tablero en sí
    __size: int  # Tamaño del tablero
    
    EMPTY_SPACE = "."  # Constante de clase que marca los espacios vacíos

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

    def __str__(self) -> str:
        """Función que es llamada cuando se hace str(self)"""
        # Cantidad de caracteres para la columna con número de fila
        offset = math.ceil(math.log10(self.__size))
        # Primera línea
        board = " "*offset + " "
        board += " ".join(chr(ord('A') + i) for i in range(self.__size)) + "\n"
        for i, line in enumerate(self.__places, 1):
            # Falta arreglar el ancho del primer número
            board += f"{i} " + " ".join(line) + '\n'
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
        # En relidad, Python le cambia internamente el nombre, porque no tiene
        # el concepto real de atributo o método privado
        if 1 > r or r > self.__size:
            return False
        return True

    def in_bounds(self, r: int, c: int) -> bool:              
        """Valida que la coordenada (r, c) esté dentro del tablero
        
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
                raise ValueError("Cooordinates with too many dimensions")
            # Si la fila está fuera de rangoo
            if not self.__check_valid_range(subscript[0]):
                raise LookupError(f"Row out of range: {subscript[0]}")
            # Si la columna está fuera de rango
            if not  self.__check_valid_range(subscript[1]):
                raise LookupError(f"Column out of range: {subscript[1]}")
            return self.__places[subscript[0] - 1][subscript[1] - 1]
        elif isinstance(subscript, int):
            # Si es un entero
            if not self.__check_valid_range(subscript):
                raise LookupError(f"Row out of range: {subscript}")
            return self.__places[subscript - 1]
        else:
            # Si el índice no es del tipo correcto
            raise TypeError("Subscript must be integer or coordinates")
    
    def __setitem__(self, key: tuple, value: str) ->  None:
        """Implementa self[key] = value
        
        El "índice" `key` tiene que ser un par de coordenadas
        """
        if not isinstance(key, tuple):
            raise TypeError(f"Subscript must be coordinates (tuple), not {type(key)}")
        if len(key) != 2:
            raise ValueError("Cooordinates with too many dimensions")
        # Si la fila está fuera de rangoo
        if not self.__check_valid_range(key[0]):
            raise LookupError(f"Row out of range: {key[0]}")
        # Si la columna está fuera de rango
        if not  self.__check_valid_range(key[1]):
            raise LookupError(f"Column out of range: {key[1]}")
        self.__places[key[0] - 1][key[1] - 1] = value

    def valid_move(self, r: int, c: int):
        """Valida que sea un movimiento válido, es decir, a una casilla libre
        
        Este método debería ser sobrecargado por un tablero hijo que
        permite movimientos válidos con otras reglas
        """
        return self[r, c] == Board.EMPTY_SPACE


# Test
if __name__ == "__main__":
    b = Board(5)
    print(b)
    print(b[5])
    print(b[3, 2])
    print([b])
    b[3, 2] = "A"
    b[1, 4] = "B"
    print(b)
    b[0]

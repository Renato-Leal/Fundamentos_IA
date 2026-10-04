% =====================================================
% BASE DE CONOCIMIENTO: JUEGOS DE MESA
% Chatbot de especificaciones técnicas y recomendación
% =====================================================

% ---------- JUEGOS (identificador, nombre para mostrar) ----------
juego(catan,       'Catán').
juego(uno,         'UNO').
juego(colo_colo,   'Colo-Colo 100 años (edición especial)').
juego(carcassonne, 'Carcassonne').
juego(dobble,      'Dobble').
juego(ticket,      'Ticket to Ride').
juego(dnd,         'Dungeons & Dragons (caja de inicio)').
juego(black_stories, 'Black Stories').
juego(dixit, 'Dixit').
juego(monopoly, 'Monopoly').
juego(scrabble, 'Scrabble').

% ---------- NÚMERO DE JUGADORES ----------
% min_jugadores(Juego, Minimo)
min_jugadores(catan, 3).
min_jugadores(uno, 2).
min_jugadores(colo_colo, 2).      % VERIFICAR con la caja
min_jugadores(carcassonne, 2).
min_jugadores(dobble, 2).
min_jugadores(ticket, 2).
min_jugadores(dnd, 2).
min_jugadores(black_stories, 2).
min_jugadores(dixit, 3).
min_jugadores(monopoly, 2).
min_jugadores(scrabble, 2).

% max_jugadores(Juego, Maximo)
max_jugadores(catan, 4).          % con ampliación 5-6 llega a 6
max_jugadores(uno, 10).
max_jugadores(colo_colo, 6).      % VERIFICAR con la caja
max_jugadores(carcassonne, 5).
max_jugadores(dobble, 8).
max_jugadores(ticket, 5).
max_jugadores(dnd, 7).
max_jugadores(black_stories, 30).
max_jugadores(dixit, 8).
max_jugadores(monopoly, 8).
max_jugadores(scrabble, 4).

% ---------- NIVEL DE DIFICULTAD (facil, medio, dificil) ----------
dificultad(catan, medio).
dificultad(uno, facil).
dificultad(colo_colo, facil).     % VERIFICAR
dificultad(carcassonne, medio).
dificultad(dobble, facil).
dificultad(ticket, medio).
dificultad(dnd, dificil).
dificultad(dark_stories, medio).
dificultad(dixit, facil).
dificultad(monopoly, medio).
dificultad(scrabble, medio).

% ---------- CATEGORÍA (estrategia, casual, rol, cartas, trivia...) ----------
categoria(catan, estrategia).
categoria(uno, casual).
categoria(uno, cartas).
categoria(colo_colo, casual).     % VERIFICAR
categoria(carcassonne, estrategia).
categoria(dobble, casual).
categoria(dobble, reflejos).
categoria(ticket, estrategia).
categoria(dnd, rol).
categoria(dark_stories, casual).
categoria(dark_stories, cartas).
categoria(dixit, casual).
categoria(monopoly, estrategia).
categoria(scrabble, estrategia).

% ---------- REQUIERE TABLERO (si / no) ----------
requiere_tablero(catan, si).
requiere_tablero(uno, no).
requiere_tablero(colo_colo, si).  % VERIFICAR
requiere_tablero(carcassonne, no).  % se arma con fichas, sin tablero fijo
requiere_tablero(dobble, no).
requiere_tablero(ticket, si).
requiere_tablero(dnd, no).        % mapa opcional
requiere_tablero(dark_stories, no).
requiere_tablero(dixit, si).
requiere_tablero(monopoly, si). 
requiere_tablero(scrabble, si).

% ---------- TIEMPO CRONOMETRADO ----------
% tiempo_cronometrado(Juego, no)  o  tiempo_cronometrado(Juego, Minutos)
tiempo_cronometrado(catan, no).
tiempo_cronometrado(uno, no).
tiempo_cronometrado(colo_colo, no).  % VERIFICAR
tiempo_cronometrado(carcassonne, no).
tiempo_cronometrado(dobble, no).
tiempo_cronometrado(ticket, no).
tiempo_cronometrado(dnd, no).
tiempo_cronometrado(dark_stories, no).
tiempo_cronometrado(dixit, no).
tiempo_cronometrado(monopoly, no).
tiempo_cronometrado(scrabble, no).

% Duración aproximada de una partida, en minutos
duracion_minutos(catan, 75).
duracion_minutos(uno, 30).
duracion_minutos(colo_colo, 45).     % VERIFICAR
duracion_minutos(carcassonne, 45).
duracion_minutos(dobble, 15).
duracion_minutos(ticket, 60).
duracion_minutos(dnd, 180).
duracion_minutos(dark_stories, 20).
duracion_minutos(dixit, 30).
duracion_minutos(monopoly, 100).
duracion_minutos(scrabble, 90).

% ---------- EDAD MÍNIMA (años) ----------
edad_minima(catan, 10).
edad_minima(uno, 7).
edad_minima(colo_colo, 8).        % VERIFICAR
edad_minima(carcassonne, 7).
edad_minima(dobble, 6).
edad_minima(ticket, 8).
edad_minima(dnd, 12).
edad_minima(dark_stories, 12).
edad_minima(dixit, 8).
edad_minima(monopoly, 8).
edad_minima(scrabble, 10).

% ---------- TIENE EXPANSIÓN (si / no) ----------
tiene_expansion(catan, si).       % Navegantes, Ciudades y Caballeros, Ampliación 5-6
tiene_expansion(uno, no).
tiene_expansion(colo_colo, no).   % VERIFICAR
tiene_expansion(carcassonne, si).
tiene_expansion(dobble, no).
tiene_expansion(ticket, si).
tiene_expansion(dnd, si).
tiene_expansion(dark_stories, no).
tiene_expansion(dixit, si).
tiene_expansion(monopoly, no).
tiene_expansion(scrabble, no).

% ---------- IDIOMA (es / en); un juego puede tener varios ----------
idioma(catan, es).
idioma(catan, en).
idioma(uno, es).
idioma(uno, en).
idioma(colo_colo, es).
idioma(carcassonne, es).
idioma(carcassonne, en).
idioma(dobble, es).
idioma(dobble, en).
idioma(ticket, es).
idioma(ticket, en).
idioma(dnd, es).
idioma(dnd, en).
idioma(dark_stories, es).
idioma(dark_stories, en).
idioma(dixit, es).
idioma(dixit, en).
idioma(monopoly, es).
idioma(monopoly, en).
idioma(scrabble, en).
idioma(scrabble, es).

% =====================================================
% REGLAS
% =====================================================

% --- Regla 1: la cantidad de jugadores NO es válida ---
% si jugadores_usuario < min O jugadores_usuario > max
jugadores_invalidos(Juego, N) :-
    min_jugadores(Juego, Min),
    N < Min.
jugadores_invalidos(Juego, N) :-
    max_jugadores(Juego, Max),
    N > Max.

jugadores_validos(Juego, N) :-
    \+ jugadores_invalidos(Juego, N).

% --- Regla 2: el usuario es menor que la edad mínima ---
edad_invalida(Juego, EdadUsuario) :-
    edad_minima(Juego, EdadMin),
    EdadUsuario < EdadMin.

edad_valida(Juego, EdadUsuario) :-
    \+ edad_invalida(Juego, EdadUsuario).

% --- Regla 3: se puede jugar (cumple jugadores y edad) ---
% Para un grupo con varias edades, usa la edad del más pequeño.
puede_jugar(Juego, N, Edad) :-
    juego(Juego, _),
    jugadores_validos(Juego, N),
    edad_valida(Juego, Edad).

% --- Regla 4: recomendación por categoría ---
recomendar(Juego, N, Edad, Categoria) :-
    puede_jugar(Juego, N, Edad),
    categoria(Juego, Categoria).

% --- Regla 5: recomendación según tablero ---
recomendar_con_tablero(Juego, N, Edad, Tablero) :-
    puede_jugar(Juego, N, Edad),
    requiere_tablero(Juego, Tablero).

% --- Regla 6: juegos rápidos (duración máxima en minutos) ---
recomendar_rapido(Juego, N, Edad, MaxMin) :-
    puede_jugar(Juego, N, Edad),
    duracion_minutos(Juego, D),
    D =< MaxMin.

% --- Regla 7: juego cronometrado ---
es_cronometrado(Juego) :-
    tiempo_cronometrado(Juego, T),
    T \= no.

% --- Regla 8: por idioma ---
recomendar_idioma(Juego, N, Edad, Idioma) :-
    puede_jugar(Juego, N, Edad),
    idioma(Juego, Idioma).

% --- Explicación de por qué NO se puede jugar (útil para el chatbot) ---
motivo_rechazo(Juego, N, _, 'faltan jugadores') :-
    min_jugadores(Juego, Min), N < Min.
motivo_rechazo(Juego, N, _, 'sobran jugadores') :-
    max_jugadores(Juego, Max), N > Max.
motivo_rechazo(Juego, _, Edad, 'edad menor a la minima') :-
    edad_minima(Juego, EdadMin), Edad < EdadMin.

% =====================================================
% EJEMPLOS DE CONSULTAS
% =====================================================
% ?- puede_jugar(J, 4, 9).                  % ¿qué juegos para 4 jugadores, el menor de 9 años?
% ?- recomendar(J, 3, 12, rol).             % juegos de rol para 3 jugadores de 12 años
% ?- jugadores_invalidos(catan, 2).         % true
% ?- edad_invalida(dnd, 10).                % true
% ?- motivo_rechazo(catan, 2, 8, M).        % M = 'faltan jugadores' ; M = 'edad menor a la minima'
% ?- recomendar_rapido(J, 4, 8, 30).        % juegos de hasta 30 min
% ?- recomendar_idioma(J, 2, 10, en).       % juegos disponibles en inglés
% ?- juego(J, Nombre), tiene_expansion(J, si).

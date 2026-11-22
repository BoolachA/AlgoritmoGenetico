"""
datos.py  —  Persona A
======================
Carga del problema TSP y funciones base que usa el resto del algoritmo genético:

    leer_tsp(ruta)                      -> lista de ciudades (id, x, y)
    matriz_distancias(ciudades)         -> matriz NxN con todas las distancias
    distancia_ruta(ruta, D)             -> longitud total de un recorrido (aptitud "bruta")
    poblacion_inicial(n, tam, semilla)  -> lista de cromosomas aleatorios

CONVENIO IMPORTANTE (acordado con Persona B):
    Dentro del programa las ciudades se identifican por su ÍNDICE 0..N-1
    (posición en la lista que devuelve leer_tsp), NO por el id 1..N del fichero.
    Así un cromosoma se puede usar directamente para indexar la matriz D.
    Para mostrar resultados con los ids del fichero basta con sumar 1.

    Un cromosoma es una permutación de [0, 1, ..., N-1] SIN repetir la primera
    ciudad al final: la vuelta al origen la añade distancia_ruta().
"""

import numpy as np


def leer_tsp(ruta_fichero):
    """
    Lee un fichero en formato TSPLIB (.tsp) y devuelve la lista de ciudades.

    Recorre el fichero línea a línea (algoritmo ITERATIVO) y solo guarda las
    líneas que hay entre 'NODE_COORD_SECTION' y 'EOF'.

    Parámetros
    ----------
    ruta_fichero : str
        Ruta al fichero .tsp (p. ej. "data/qa194.tsp").

    Devuelve
    --------
    list[tuple[int, float, float]]
        Lista de tuplas (id, x, y) en el orden del fichero.
        Ejemplo: [(1, 24748.3333, 50840.0), (2, 24758.8889, 51211.9444), ...]
    """
    ciudades = []
    leyendo_coordenadas = False

    with open(ruta_fichero, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()

            if not linea:                       # línea vacía -> se ignora
                continue
            if linea == "EOF":                  # fin de los datos
                break
            if linea.startswith("NODE_COORD_SECTION"):
                leyendo_coordenadas = True      # a partir de aquí vienen las ciudades
                continue

            if leyendo_coordenadas:
                partes = linea.split()
                id_ciudad = int(partes[0])
                x = float(partes[1])
                y = float(partes[2])
                ciudades.append((id_ciudad, x, y))

    return ciudades


def matriz_distancias(ciudades, redondear_tsplib=False):
    """
    Calcula UNA SOLA VEZ la distancia euclídea entre todos los pares de ciudades
    y la guarda en una matriz D, donde D[i][j] = distancia entre la ciudad i y la j.

    Esto cubre el requisito del enunciado de "guardar las distancias repetidas":
    en vez de recalcular sqrt((x1-x2)^2 + (y1-y2)^2) cada vez que un cromosoma
    usa el tramo i->j, se consulta D[i, j] (tabla de memorización).

    Parámetros
    ----------
    ciudades : list[tuple[int, float, float]]
        Salida de leer_tsp().
    redondear_tsplib : bool
        Si es True, redondea cada distancia al entero más cercano, como hace el
        estándar TSPLIB para EUC_2D. Solo hace falta para comparar exactamente
        con el óptimo publicado de qa194 (9352). Por defecto False.

    Devuelve
    --------
    np.ndarray de forma (N, N), simétrica y con ceros en la diagonal.
    """
    # Nos quedamos solo con las coordenadas: array de forma (N, 2)
    coords = np.array([(x, y) for (_, x, y) in ciudades], dtype=float)

    # Diferencias entre todos los pares a la vez (broadcasting de numpy):
    # dif[i, j] = coords[i] - coords[j]  -> forma (N, N, 2)
    dif = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]

    # d = sqrt((x1 - x2)^2 + (y1 - y2)^2)
    D = np.sqrt((dif ** 2).sum(axis=2))

    if redondear_tsplib:
        D = np.floor(D + 0.5)   # nint() de TSPLIB

    return D


def distancia_ruta(ruta, D):
    """
    Longitud total del recorrido, INCLUYENDO la vuelta a la ciudad de partida.
    Es la aptitud "bruta" del cromosoma: cuanto MENOR, mejor.
    (La transformación a aptitud positiva "mayor = mejor" para la ruleta se
    hace en seleccion.py.)

    Parámetros
    ----------
    ruta : list[int] | np.ndarray
        Cromosoma: permutación de índices 0..N-1.
    D : np.ndarray
        Matriz de distancias de matriz_distancias().

    Devuelve
    --------
    float
    """
    ruta = np.asarray(ruta)
    # np.roll(ruta, -1) desplaza la ruta una posición: [a, b, c] -> [b, c, a]
    # Así emparejamos cada ciudad con la siguiente, y la última con la primera
    # (vuelta al origen). D[origenes, destinos] coge todos los tramos de golpe.
    siguientes = np.roll(ruta, -1)
    return float(D[ruta, siguientes].sum())


def poblacion_inicial(n_ciudades, tam_poblacion, semilla=None):
    """
    Genera la población inicial como permutaciones aleatorias de las ciudades
    (apartado VI del enunciado).

    Parámetros
    ----------
    n_ciudades : int
        Número de ciudades (194 para Qatar).
    tam_poblacion : int
        Número de cromosomas a generar.
    semilla : int | None
        Semilla aleatoria para que los experimentos sean reproducibles.

    Devuelve
    --------
    list[list[int]]
        Lista de cromosomas; cada uno es una permutación de 0..n_ciudades-1.
    """
    rng = np.random.default_rng(semilla)
    return [rng.permutation(n_ciudades).tolist() for _ in range(tam_poblacion)]


# Prueba rápida al ejecutar directamente:  python src/datos.py
if __name__ == "__main__":
    ciudades = leer_tsp("data/qa194.tsp")
    D = matriz_distancias(ciudades)
    pob = poblacion_inicial(len(ciudades), 5, semilla=42)
    print(f"Ciudades leídas: {len(ciudades)}")
    print(f"Primera: {ciudades[0]}  Última: {ciudades[-1]}")
    for i, crom in enumerate(pob):
        print(f"Cromosoma {i}: distancia = {distancia_ruta(crom, D):,.2f}")

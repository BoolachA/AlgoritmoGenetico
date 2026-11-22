"""datos.py — Persona A. Lectura del .tsp, distancias, aptitud y población inicial."""


def leer_tsp(ruta_fichero):
    """Devuelve list[(id, x, y)]."""
    raise NotImplementedError


def matriz_distancias(ciudades):
    """Devuelve np.ndarray NxN con D[i, j] = distancia entre ciudad i y j."""
    raise NotImplementedError


def distancia_ruta(ruta, D):
    """Longitud total del recorrido (incluye la vuelta al origen). Menor = mejor."""
    raise NotImplementedError


def poblacion_inicial(n_ciudades, tam_poblacion, semilla=None):
    """Devuelve list[list[int]], permutaciones aleatorias de 0..n_ciudades-1."""
    raise NotImplementedError

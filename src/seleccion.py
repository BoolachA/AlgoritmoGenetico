"""seleccion.py — Persona A. Selección por ruleta."""


def seleccion_ruleta(poblacion, distancias, k):
    """
    Elige k cromosomas de la población con probabilidad proporcional a su aptitud
    (aptitud positiva y mayor = mejor, derivada de la distancia).

    poblacion  : list[list[int]]
    distancias : list[float]   (distancia_ruta de cada cromosoma, mismo orden)
    k          : int
    Devuelve   : list[list[int]]  (k cromosomas seleccionados)
    """
    raise NotImplementedError

"""seleccion.py — Persona A. Selección por ruleta."""

import random
from bisect import bisect_left
from itertools import accumulate

# "inversa": aptitud = 1 / distancia (diferencias suaves entre rutas)
# "ventana": aptitud = peor distancia - distancia (favorece más a las mejores)
APTITUD = "ventana"


def seleccion_ruleta(poblacion, distancias, k):
    """
    Elige k cromosomas de la población con probabilidad proporcional a su aptitud
    (aptitud positiva y mayor = mejor, derivada de la distancia).

    poblacion  : list[list[int]]
    distancias : list[float]   (distancia_ruta de cada cromosoma, mismo orden)
    k          : int
    Devuelve   : list[list[int]]  (k cromosomas seleccionados)
    """
    # 1. Aptitud de cada individuo (siempre positiva)
    if APTITUD == "inversa":
        aptitudes = [1 / d for d in distancias]
    else:
        peor = max(distancias)
        # el + 1e-9 evita que la suma sea 0 si todas las rutas miden igual
        aptitudes = [peor - d + 1e-9 for d in distancias]

    # 2 y 3. Aptitud total y probabilidad de cada individuo
    total = sum(aptitudes)
    probabilidades = [a / total for a in aptitudes]

    # 4. Probabilidades acumuladas
    acumuladas = list(accumulate(probabilidades))

    # 5 y 6. Girar la ruleta k veces
    seleccionados = []
    for _ in range(k):
        r = random.random()
        # primer individuo cuya probabilidad acumulada es >= r
        # (min protege del redondeo: la última suma puede quedar en 0.999999)
        i = min(bisect_left(acumuladas, r), len(poblacion) - 1)
        seleccionados.append(list(poblacion[i]))
    return seleccionados
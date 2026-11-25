"""operadores.py — Persona B. Mutación por inversión y cruzamiento por ciclos."""

import random


def mutacion_inversion(ruta):
    """Invierte una subcadena aleatoria. Devuelve una ruta nueva."""
    hijo = list(ruta)  # copia: no se modifica el original
    if len(hijo) < 2:
        return hijo
    # Dos cortes distintos, ordenados. La subcadena es hijo[i:j] (j no incluido)
    i, j = sorted(random.sample(range(len(hijo) + 1), 2))
    while j - i < 2:  # invertir un solo elemento no cambiaría nada
        i, j = sorted(random.sample(range(len(hijo) + 1), 2))
    hijo[i:j] = hijo[i:j][::-1]
    return hijo


def _buscar_ciclo(padre1, padre2, posicion_en_p1, i, ciclo):
    """
    ALGORITMO RECURSIVO: recorre el ciclo que pasa por la posición i.
    Caso base: la posición ya está en el ciclo (se ha cerrado).
    Caso recursivo: saltar a la posición que ocupa padre2[i] en padre1.
    """
    if i in ciclo:
        return ciclo
    ciclo.add(i)
    siguiente = posicion_en_p1[padre2[i]]
    return _buscar_ciclo(padre1, padre2, posicion_en_p1, siguiente, ciclo)


def _crear_hijo(padre1, padre2):
    """Posiciones del primer ciclo: de padre1. El resto: de padre2."""
    posicion_en_p1 = {ciudad: i for i, ciudad in enumerate(padre1)}
    ciclo = _buscar_ciclo(padre1, padre2, posicion_en_p1, 0, set())
    return [padre1[i] if i in ciclo else padre2[i] for i in range(len(padre1))]


def cruce_ciclos(padre1, padre2):
    """Cruzamiento por ciclos (CX). Devuelve (hijo1, hijo2)."""
    # El segundo hijo es el mismo proceso con los padres intercambiados
    return _crear_hijo(padre1, padre2), _crear_hijo(padre2, padre1)
"""ag.py — Persona B. Bucle principal del algoritmo genético."""

import random

from operadores import cruce_ciclos, mutacion_inversion

# AJUSTAR: nombres de los módulos y funciones de Persona A
from datos import distancia_ruta      # distancia_ruta(ruta, D) -> float
from datos import poblacion_inicial  # poblacion_inicial(n, tam) -> lista de rutas
from seleccion import seleccion_ruleta   # seleccion_ruleta(poblacion, distancias) -> ruta


def algoritmo_genetico(D, tam_poblacion, prob_cruce, prob_mutacion, n_elite,
                       max_generaciones, semilla=None):
    """
    Devuelve (mejor_ruta, historial) donde historial es una lista con la
    mejor distancia de cada generación (la usan las gráficas de Persona A).

    prob_cruce y prob_mutacion van entre 0 y 1.
    historial[0] es la población inicial: tiene max_generaciones + 1 valores.
    """
    if not 0 <= n_elite <= tam_poblacion:
        raise ValueError("n_elite debe estar entre 0 y tam_poblacion")
    if semilla is not None:
        random.seed(semilla)  # permite repetir un experimento

    # Población inicial y su evaluación
    poblacion = poblacion_inicial(len(D), tam_poblacion)
    distancias = [distancia_ruta(r, D) for r in poblacion]

    mejor_distancia = min(distancias)
    mejor_ruta = list(poblacion[distancias.index(mejor_distancia)])
    historial = [mejor_distancia]

    # ALGORITMO ITERATIVO: una vuelta por generación.
    # Criterio de paro: alcanzar max_generaciones.
    for _ in range(max_generaciones):
        # Elitismo: los n_elite mejores pasan sin cambios
        orden = sorted(range(len(poblacion)), key=lambda i: distancias[i])
        nueva = [list(poblacion[i]) for i in orden[:n_elite]]

        while len(nueva) < tam_poblacion:
            # Selección
            padre1 = seleccion_ruleta(poblacion, distancias)
            padre2 = seleccion_ruleta(poblacion, distancias)

            # Cruzamiento
            if random.random() < prob_cruce:
                hijos = cruce_ciclos(padre1, padre2)
            else:
                hijos = (list(padre1), list(padre2))

            # Mutación
            for hijo in hijos:
                if len(nueva) == tam_poblacion:
                    break
                if random.random() < prob_mutacion:
                    hijo = mutacion_inversion(hijo)
                nueva.append(hijo)

        # Evaluación de la nueva generación
        poblacion = nueva
        distancias = [distancia_ruta(r, D) for r in poblacion]

        mejor_actual = min(distancias)
        historial.append(mejor_actual)
        if mejor_actual < mejor_distancia:
            mejor_distancia = mejor_actual
            mejor_ruta = list(poblacion[distancias.index(mejor_actual)])

    return mejor_ruta, historial
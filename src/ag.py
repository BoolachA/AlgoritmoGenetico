"""ag.py — Persona B. Bucle principal del algoritmo genético."""

import random

from operadores import cruce_ciclos, mutacion_inversion

import datos
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

        
        # Selección: se eligen de una vez todos los padres (número par)
        n_hijos = tam_poblacion - len(nueva)
        padres = seleccion_ruleta(poblacion, distancias, n_hijos + n_hijos % 2)

        for p in range(0, len(padres), 2):
            padre1, padre2 = padres[p], padres[p + 1]
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

if __name__ == "__main__":
    ciudades = datos.leer_tsp("../data/qa194.tsp")
    D = datos.matriz_distancias(ciudades)

    mejor_ruta, historial = algoritmo_genetico(
        D, tam_poblacion=50, prob_cruce=0.8, prob_mutacion=0.2,
        n_elite=2, max_generaciones=500, semilla=42)
    print(historial[0], "->", historial[-1])
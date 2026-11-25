"""
Tests de operadores.py, seleccion.py y ag.py.
Ejecutar desde la carpeta raíz del repo con:   python -m pytest
o sin pytest con:                              python tests/test_ag.py
"""
import os
import random
import sys

# Permite importar los módulos de src/ aunque se ejecute el test directamente
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "src"))

from ag import algoritmo_genetico
from datos import matriz_distancias, distancia_ruta
from operadores import mutacion_inversion, cruce_ciclos
from seleccion import seleccion_ruleta


def _matriz_prueba(n=20):
    rng = random.Random(0)
    ciudades = [(i + 1, rng.random() * 100, rng.random() * 100) for i in range(n)]
    return matriz_distancias(ciudades)


def test_cruce_ejemplo_enunciado():
    p1 = [3, 1, 2, 6, 4, 5, 7, 9, 8]
    p2 = [4, 5, 2, 1, 8, 7, 6, 9, 3]
    hijo1, hijo2 = cruce_ciclos(p1, p2)
    assert hijo1 == [3, 5, 2, 1, 4, 7, 6, 9, 8]
    assert hijo2 == [4, 1, 2, 6, 8, 5, 7, 9, 3]


def test_cruce_hijos_validos():
    random.seed(1)
    for _ in range(200):
        p1 = random.sample(range(194), 194)
        p2 = random.sample(range(194), 194)
        for hijo in cruce_ciclos(p1, p2):
            assert sorted(hijo) == list(range(194))


def test_mutacion_inversion():
    random.seed(1)
    original = list(range(10))
    for _ in range(200):
        hijo = mutacion_inversion(original)
        assert original == list(range(10))        # no modifica el padre
        assert sorted(hijo) == original           # sigue siendo permutación
        # Lo que ha cambiado es un único tramo invertido
        cambios = [i for i in range(10) if hijo[i] != original[i]]
        i, j = cambios[0], cambios[-1] + 1
        assert hijo[i:j] == original[i:j][::-1]


def test_ruleta():
    random.seed(1)
    poblacion = [[0, 1, 2], [0, 2, 1], [1, 0, 2]]
    elegidos = seleccion_ruleta(poblacion, [10.0, 20.0, 30.0], 3000)
    assert len(elegidos) == 3000
    assert all(c in poblacion for c in elegidos)
    # La ruta más corta sale más veces que la más larga
    assert elegidos.count(poblacion[0]) > elegidos.count(poblacion[2])


def test_ag_resultado():
    D = _matriz_prueba()
    ruta, historial = algoritmo_genetico(D, 30, 0.8, 0.2, 2, 50, semilla=42)
    assert sorted(ruta) == list(range(20))
    assert len(historial) == 51                   # población inicial + 50 generaciones
    # Con elitismo la mejor distancia nunca empeora
    assert all(a >= b - 1e-9 for a, b in zip(historial, historial[1:]))
    assert abs(distancia_ruta(ruta, D) - historial[-1]) < 1e-9


def test_ag_reproducible():
    D = _matriz_prueba()
    primera = algoritmo_genetico(D, 30, 0.8, 0.2, 2, 20, semilla=7)
    segunda = algoritmo_genetico(D, 30, 0.8, 0.2, 2, 20, semilla=7)
    assert primera == segunda


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print("OK", nombre)
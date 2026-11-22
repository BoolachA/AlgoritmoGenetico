"""
Tests de datos.py (Persona A).
Ejecutar desde la carpeta raíz del repo con:   python -m pytest
o sin pytest con:                              python tests/test_datos.py
"""
import os
import sys

import numpy as np

# Permite importar src/ aunque se ejecute el test directamente
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from src.datos import leer_tsp, matriz_distancias, distancia_ruta, poblacion_inicial

RUTA_TSP = os.path.join(RAIZ, "data", "qa194.tsp")


def test_leer_tsp():
    ciudades = leer_tsp(RUTA_TSP)
    assert len(ciudades) == 194
    assert ciudades[0] == (1, 24748.3333, 50840.0)
    assert ciudades[-1] == (194, 26150.2778, 51108.0556)


def test_triangulo_3_4_5():
    # Triángulo rectángulo de lados 3, 4 y 5 -> perímetro 12 (calculable a mano)
    ciudades = [(1, 0.0, 0.0), (2, 3.0, 0.0), (3, 3.0, 4.0)]
    D = matriz_distancias(ciudades)
    assert D[0, 1] == 3 and D[1, 2] == 4 and D[0, 2] == 5
    assert distancia_ruta([0, 1, 2], D) == 12
    # Empezar en otra ciudad o recorrer al revés da la misma longitud
    assert distancia_ruta([2, 0, 1], D) == 12
    assert distancia_ruta([2, 1, 0], D) == 12


def test_matriz_simetrica():
    D = matriz_distancias(leer_tsp(RUTA_TSP))
    assert D.shape == (194, 194)
    assert np.allclose(D, D.T)
    assert np.all(np.diag(D) == 0)


def test_poblacion_valida():
    pob = poblacion_inicial(194, 50, semilla=1)
    assert len(pob) == 50
    for crom in pob:
        assert sorted(crom) == list(range(194))   # permutación: sin repetidos ni huecos
    # Con la misma semilla sale la misma población (reproducibilidad)
    assert pob == poblacion_inicial(194, 50, semilla=1)


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print("OK", nombre)

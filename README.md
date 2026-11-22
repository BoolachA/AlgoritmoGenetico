# Algoritmo genético para el TSP (Qatar, 194 ciudades)

Proyecto de Lógica, algoritmia y computación. Selección por ruleta, mutación por inversión y cruzamiento por ciclos.

## Estructura
- `data/qa194.tsp` – datos del problema
- `src/datos.py` – lectura, matriz de distancias, aptitud, población inicial (Persona A)
- `src/seleccion.py` – selección por ruleta (Persona A)
- `src/operadores.py` – mutación por inversión y cruce por ciclos (Persona B)
- `src/ag.py` – bucle principal del algoritmo genético (Persona B)
- `notebook_entrega.ipynb` – notebook final que importa de `src/`

## Convenio
Las ciudades se identifican por índice 0..N-1. Un cromosoma es una permutación de 0..N-1
sin repetir la primera ciudad al final (la vuelta la suma `distancia_ruta`).

## Uso
    pip install -r requirements.txt
    python -m pytest

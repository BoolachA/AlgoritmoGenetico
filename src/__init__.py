# Paquete src: código del algoritmo genético
import datos
import ag

ciudades = datos.leer_tsp("../data/qa194.tsp")
D = datos.matriz_distancias(ciudades)

mejor_ruta, historial = ag.algoritmo_genetico(
    D, tam_poblacion=100, prob_cruce=0.8, prob_mutacion=0.2,
    n_elite=2, max_generaciones=2000, semilla=42)
print(historial[0], "->", historial[-1])
#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Clase dedicada a la implementación de la metaheurística MMC'''


import math
from compositor import Compositor, UPPER_BOUND, LOWER_BOUND
import random


FCLA = 0.9   # Factor para establecer enlaces 
IFG = 0.25   # Probabilidad de generar una melodía sin tener en cuenta el conocimiento adquirido
CFG = 0.25   # Probabilidad de generar un valor sin tener en cuenta el conocimiento adquirido

NUM_COMPOSITORS = 5
NUM_TUNES = 100
NUM_CHORDS = 10

NUM_ITERATIONS = 1500

COMPOSITORS = []   # Sociedad de compositores
SOLUTION_SET = []   # Conjunto de mejores soluciones de cada compositor


def main():
    generate_society()   # Se genera la sociedad de compositores

    for i in range(NUM_COMPOSITORS):
        COMPOSITORS[i].initialize_artwork()   # Se genera una obra para cada compositor

    current_iteration = 1
    criterion_is_met = False
    while not criterion_is_met:
        for comp in range(NUM_COMPOSITORS):
            update_society(current_iteration)    # Se actualizan los enlaces entre compositores
            information_exchange(current_iteration)   # Intercambio de información entre compositores

            for i in range(NUM_COMPOSITORS):
                build_background_knowledge()
                new_tune = generate_new_tune(i)
                new_tune_score = evaluate_tune(new_tune)
                i_worst, i_worst_score = get_worst_tune(i)

                # Se sustituye la peor melodía del compositor si la nueva es mejor
                if new_tune_score < i_worst_score:
                    for j in range(len(COMPOSITORS[i].artwork)):
                        if i_worst == COMPOSITORS[i].artwork[j]:
                            COMPOSITORS[i].artwork[j] = new_tune
                
                COMPOSITORS[i].clear()   # Se reinician las matrices de conocimiento de los agentes

            current_iteration += 1
            if current_iteration > NUM_ITERATIONS:   # Se comprueba la condición de parada
                criterion_is_met = True


    # Se obtiene la mejor solución de cada compositor
    for i in range(NUM_COMPOSITORS):
        best_tune, best_tune_score = get_best_tune(i)
        SOLUTION_SET.append(best_tune)

    best_solution = None
    best_solution_score = 100000
    best_solution_index = None

    print('\n\nSOLUCIÓN')
    for i in range(len(SOLUTION_SET)):
        current_score = evaluate_tune(SOLUTION_SET[i])
        total_sum = sum_tune(SOLUTION_SET[i])
        print('Compositor ' + str(i) + ': ' + str(SOLUTION_SET[i]) + \
            ' | Suma total: ' + str(total_sum) +
            ' | Aptitud de la melodía: ' + str(round(current_score,2)))

        if current_score < best_solution_score:
            best_solution = SOLUTION_SET[i]
            best_solution_index = i
            best_solution_score = current_score

    print('\n\nMEJOR SOLUCIÓN')
    current_score = evaluate_tune(best_solution)
    total_sum = sum_tune(best_solution)
    print('Compositor ' + str(best_solution_index) + ': ' + str(best_solution) + \
            ' | Suma total: ' + str(total_sum) +
            ' | Aptitud de la melodía: ' + str(round(current_score,2)))

    print('\n\nNOTA: dado que el MMC trata de buscar mínimos en funciones, y nuestra \
función es la raíz de la suma de todos los valores, se persigue que el vector \
obtenido tenga los mínimos valores posibles, y más próximos a 0.')


def generate_society():
    '''Genera un número definido de compositores'''

    for i in range(NUM_COMPOSITORS):
        new_compositor = Compositor(i,NUM_COMPOSITORS,NUM_TUNES,NUM_CHORDS)
        COMPOSITORS.append(new_compositor)


def update_society(current_iteration):
    '''Actualiza los enlaces entre compositores, determinados por variables booleanas'''

    print('ACTUALIZACIÓN DE VECINOS DE LA ITERACIÓN ' + str(current_iteration))

    if current_iteration == 1:
        for i in range(NUM_COMPOSITORS):
            for k in range(NUM_COMPOSITORS):
                if i == k:
                    COMPOSITORS[i].neighbours[i] = False
                else:
                    rand_float = random.uniform(0.0,1.0)
                    if rand_float < 0.5:
                        COMPOSITORS[i].neighbours[k] = True
                        COMPOSITORS[k].neighbours[i] = True
    else:
        for i in range(NUM_COMPOSITORS):
            rand_float = random.uniform(0.0,1.0)

            if rand_float < FCLA:
                compositor_k = random.randint(0,NUM_COMPOSITORS-1)

                while compositor_k == i:
                    compositor_k = random.randint(0,NUM_COMPOSITORS-1)

                # Cambio de enlace entre vecinos
                if COMPOSITORS[i].neighbours[compositor_k] == False and i != compositor_k:
                    COMPOSITORS[i].neighbours[compositor_k] = True
                    COMPOSITORS[compositor_k].neighbours[i] = True
                    print('¡Ahora ' + str(i) + ' es vecino de ' + str(compositor_k) + '!')
                elif COMPOSITORS[i].neighbours[compositor_k] == True and i != compositor_k:
                    COMPOSITORS[i].neighbours[compositor_k] = False
                    COMPOSITORS[compositor_k].neighbours[i] = False
                    print(str(i) + ' ya no es vecino de ' + str(compositor_k) + '...')
                elif i == compositor_k:
                    COMPOSITORS[i].neighbours[compositor_k] = False
                    COMPOSITORS[compositor_k].neighbours[i] = False

    print('------------------------------------------------')

    
def information_exchange(current_iteration):
    '''Intercambio de información entre compositores vecinos'''

    print('INTERCAMBIO DE INFORMACIÓN DE LA ITERACIÓN ' + str(current_iteration))

    for i in range(NUM_COMPOSITORS):
        i_worst, i_worst_score = get_worst_tune(i)

        for k in range(NUM_COMPOSITORS):
            k_worst, k_worst_score = get_worst_tune(k)

            if COMPOSITORS[i].neighbours[k] == True and i != k:   # Sólo si son vecinos
                if i_worst_score < k_worst_score:
                    print(str(i) + ' intercambia información con ' + str(k) + '...')
                    rand_tune = random.randint(0,len(COMPOSITORS[k].artwork)-1)

                    # Añadimos una melodía del vecino a la matriz ISC
                    COMPOSITORS[i].ISC_matrix.append(COMPOSITORS[k].artwork[rand_tune])

    print('------------------------------------------------')


def get_worst_tune(compositor):
    '''Dado un compositor, devuelve la melodía con menor aptitud'''

    worst_tune = None
    worst_tune_score = -1

    for tune in COMPOSITORS[compositor].artwork:
        current_score = evaluate_tune(tune)
        
        if current_score > worst_tune_score:
            worst_tune_score = current_score
            worst_tune = tune

    return worst_tune, worst_tune_score


def get_best_tune(compositor):
    '''Dado un compositor, devuelve la melodía con mayor aptitud'''

    best_tune = None
    best_tune_score = 100000000

    for tune in COMPOSITORS[compositor].artwork:
        current_score = evaluate_tune(tune)
        
        if current_score < best_tune_score:
            best_tune_score = current_score
            best_tune = tune

    return best_tune, best_tune_score


def sum_tune(tune):
    '''Devuelve el sumatorio de los acordes de una melodía'''

    total_sum = 0

    for chord in tune:
        total_sum += chord

    return total_sum


def evaluate_tune(tune):
    '''Evalua una melodía, sumando todos los acordes y devolviendo su raíz'''

    return math.sqrt(sum_tune(tune))   # La raíz del total


def build_background_knowledge():
    '''Crea la matriz de conocimiento adquirido de cada agente'''

    for i in range(NUM_COMPOSITORS):
        COMPOSITORS[i].KM_matrix = COMPOSITORS[i].artwork + COMPOSITORS[i].ISC_matrix
        COMPOSITORS[i].fitness_KM_matrix.append(evaluate_tune(COMPOSITORS[i].KM_matrix[i]))


def generate_new_tune(compositor):
    '''Genera una nueva melodía'''

    new_tune = []

    rand_value = random.uniform(0.0,1.0)
    if rand_value < (1 - IFG):
        # Utilizamos información adquirida
        x_min, x_max = get_bounds_KM_matrix(compositor)
        for i in range(NUM_CHORDS):
            rand_KM = random.randint(0,len(COMPOSITORS[compositor].KM_matrix)-1)
            rand_tune_i = COMPOSITORS[compositor].KM_matrix[rand_KM]
            rand_KM = random.randint(0,len(COMPOSITORS[compositor].KM_matrix)-1)
            rand_tune_j = COMPOSITORS[compositor].KM_matrix[rand_KM]

            if rand_value < (1 - CFG):
                current_chord = generate_new_motive(rand_tune_i, rand_tune_j,
                    COMPOSITORS[compositor].KM_matrix, i)
                new_tune.append(round(abs(current_chord)))
            else:
                if rand_value < 0.5:
                    rand_chord = random.uniform(0.0,1.0)
                    current_chord = x_min + (rand_chord * (rand_tune_i[i] - x_min))
                    new_tune.append(round(abs(current_chord)))
                else:
                    rand_chord = random.uniform(0.0,1.0)
                    current_chord = x_max - (rand_chord * (x_max - rand_tune_i[i]))
                    new_tune.append(round(abs(current_chord)))
    else:
        # No utilizamos información adquirida
        for i in range(NUM_CHORDS):
            rand_chord = random.uniform(0.0,1.0)
            current_chord = UPPER_BOUND - (rand_chord * (UPPER_BOUND - LOWER_BOUND))
            new_tune.append(round(abs(current_chord)))

    return new_tune


def get_bounds_KM_matrix(i):
    '''Obtiene los valores límites de los acordes de la obra de un compositor'''

    min = 1000000
    max = -1

    for tune in COMPOSITORS[i].KM_matrix:
        for chord in tune:
            if chord < min:
                min = chord
            elif chord > max:
                max = chord

    return min, max


def generate_new_motive(rand_tune_i, rand_tune_j, KM_matrix, i):
    '''Genera un acorde nuevo'''

    rand_chord = random.uniform(0.0,1.0)
    rand_KM = random.randint(0,len(KM_matrix)-1)
    x_rand_tune = KM_matrix[rand_KM]
    rand_KM_chord = random.randint(0,len(x_rand_tune)-1)
    x_rand = x_rand_tune[rand_KM_chord]
    new_chord = x_rand + (rand_chord * ((rand_tune_i[i] - rand_tune_j[i]) - (2 * x_rand)))

    return new_chord


main()
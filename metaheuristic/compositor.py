'''Clase para el compositor'''


import random


LOWER_BOUND = 0
UPPER_BOUND = 25000


class Compositor(object):
    
    def __init__(self, id, num_neighbours, num_tunes, num_chords):
        self.id = id
        self.tunes = num_tunes
        self.chords = num_chords

        self.neighbours = []
        self.artwork = []
        self.ISC_matrix = []
        self.KM_matrix = []
        self.fitness_KM_matrix = []

        for i in range(num_neighbours):
            self.neighbours.append(False)


    def initialize_artwork(self):
        '''Inicializa la obra del compositor con valores aleatorios'''

        for i in range(self.tunes):
            new_tune = []
            for j in range(self.chords):
                rand_number = random.randint(LOWER_BOUND,UPPER_BOUND)
                new_tune.append(rand_number)
            self.artwork.append(new_tune)


    def clear(self):
        '''Resetea las matrices de conocimiento adquirido'''

        self.ISC_matrix.clear()
        self.KM_matrix.clear()
        self.fitness_KM_matrix.clear()
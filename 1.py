# matriz = lista dentro de outra lista 

import random


mapa_tiles = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B.....E............B',
    'B............B.....B',
    'B..BBBBB.....B.....B',
    'B...B........B.....B',
    'B...B..............B',
    'B...B.......BBB....B',
    'B..................B',
    'B.....BBBB.........B',
    'B.......E..........B',
    'B.............P....B',
    'B..................B',
    'B.....E............B',
    'BBBBBBBBBBBBBBBBBBBB',
]


ICONE_JOGADOR = '@'

class Mundo:
    def __init__(self):
        self.grade = [list(linha) for linha in mapa_tiles]
        self.jogador_X = 0
        self.jogador_Y = 0 
        self.inimigos = []

        for y, linha in enumerate(self.grade):
            for x, celula in enumerate(linha):
                if celula == "P":
                    self.jogador_X , self.jogador_Y = x, y
                    self.grade[x[y]] = '.'
                elif celula == 'E': 
                    self.inimigos.append([x, y])
                    self.grade[y[x]] = '.'

    def mover_Jogador(self, dx, dy):
        novo_x = self.jogador_X + dx
        novo_y = self.jogador_Y + dy
        self.jogador_X, self.jogador_Y = novo_x, novo_y

    def inimigo_em(self, x, y): 
        for inimigo in self.inimigos:
            if inimigo[0] == x and inimigo[1] == y:
                return inimigo
        return None 

    def renderizar(self):
        for y, linha in enumerate(self.grade):
            texto_linha = ''

            for x, celula in enumerate(linha):
                if (x, y) == (self.jogador_X, self.jogador_Y):
                    texto_linha += ICONE_JOGADOR# matriz = lista dentro de outra lista 


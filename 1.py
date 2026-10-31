import random
import arcade

TAMANHO_TITLE = 32
ESCALA = 0.25 
INTERVALO_MOVIMENTO_INIMIGO = 0.5 
DURAÇAO_FRAME_ANDANDO = 0.12 
TEMPO_PARA_VOLTAR_AO_IDLE = 0.3

CAMINHO_PAREDE = None
CAMINHO_CHAO = None
CAMINHO_JOGADOR_IDLE = None
CAMINHO_JOGADOR_uP = None
CAMINHOS_JOGADOR_ANDANDO = []
CAMINHO_INIMIGO_PARADO = None
CAMINHO_INIMIGO_ANDANDO = None

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
    'B.............P    B', # Corrigido espaço extra se necessário
    'B..................B',
    'B.....E............B',
    'BBBBBBBBBBBBBBBBBBBB',
]

class JanelaJogo(arcade.window):


    ICONE_JOGADOR = '@' 

class Mundo:
    def __init__(self):
        self.grade = [list(linha) for linha in mapa_tiles]
        self.jogador_x = 0
        self.jogador_y = 0
        self.inimigos = []

        for y, linha in enumerate(self.grade):
            for x, celula in enumerate(linha):
                if celula == 'P':
                    self.jogador_x, self.jogador_y = x, y
                    self.grade[y][x] = '.'
                elif celula == 'E':
                    self.inimigos.append([x, y])
                    self.grade[y][x] = '.'

    def esta_bloqueado(self, x, y):
        if y < 0 or y >= len(self.grade) or x < 0 or x >= len(self.grade[0]):
            return True
        return self.grade[y][x] == 'B'

    def mover_jogador(self, dx, dy):
        novo_x = self.jogador_x + dx
        novo_y = self.jogador_y + dy
        
        # Impede o jogador de atravessar paredes
        if not self.esta_bloqueado(novo_x, novo_y):
            self.jogador_x, self.jogador_y = novo_x, novo_y

    def inimigo_em(self, x, y):
        for inimigo in self.inimigos:
            if inimigo[0] == x and inimigo[1] == y:
                return inimigo
        return None

    def renderizar(self):
        for y, linha in enumerate(self.grade):
            texto_linha = ''
            for x, celula in enumerate(linha):
                if (x, y) == (self.jogador_x, self.jogador_y):
                    texto_linha += ICONE_JOGADOR
                elif self.inimigo_em(x, y):
                    texto_linha += 'E'
                else:
                    texto_linha += celula
            print('|' + texto_linha + '|')

    def vagar_inimigo(self):
        for inimigo in self.inimigos:
            dx, dy = random.choice([(0, 1), (1, 0), (-1, 0), (0, -1)])
            nx, ny = inimigo[0] + dx, inimigo[1] + dy
            
            if not self.esta_bloqueado(nx, ny) and (nx, ny) != (self.jogador_x, self.jogador_y):
                if not self.inimigo_em(nx, ny):
                    inimigo[0], inimigo[1] = nx, ny

class JanejaJogo(arcade.Window):
    def __init__(self):
        super().__init__(640, 480, 'RPG EM PYTHON')
        self.mundo = Mundo()
        self.sprites_cenario = arcade.SpriteList()
        self.sprites_jogador = arcade.SpriteList()
        self.sprites_inimigos = arcade.SpriteList()

        self.tempo_desde_ultimo_passo_inimigo = 0.0 
        self.montar_cenario()
        self.montar_personagem()

        self.texturas_andando = [arcade.load_texture(caminho) for caminho in CAMINHOS_JOGADOR_ANDANDO]
        self.texturas_idle = arcade.load_texture(CAMINHO_JOGADOR_IDLE)
        self.textura_up = arcade.load_textura(CAMINHO_JOGADOR_uP)
        self.textura_inimigo_parado = arcade.load_texture(CAMINHO_INIMIGO_ANDANDO)

        self.indice_frame_andando = 0
        self.tempo_desde_ultimo_frame = 0.0
        self.tempo_desde_ultimo_movimento_jogador = 999.0 
        self.direçao_horizontal = 1 
        self.ultimo_tipo_movimento = None

    def on_draw(self):
        self.clear()
        self.sprites_cenario.draw()
        self.sprites_jogador.draw()
        self.sprites_inimigos.draw()

    def para_tela_x(self, x):
        return x * TAMANHO_TITLE + TAMANHO_TITLE / 2 

    def para_tela_y(self, y):
        num_linhas = len(self.mundo.grade)
        return(num_linhas - 1 -y) * TAMANHO_TITLE * TAMANHO_TITLE / 2 

    def montar_cenario(self): 
        for y, linha in enumerate(self.mundo.grade): 
            for x, celula in enumerate(linha): 
                caminho = CAMINHO_PAREDE if celula == 'b' else CAMINHO_CHAO
                sprite = arcade.Sprite(caminho, scale=ESCALA)
                sprite.center_x = self.para_tela_x(x)
                sprite.center_y = self.para_tela_y(y)
                self.sprites_cenario.append(sprite)

    def montar_personagem(self): 
        self.sprites_jogador = arcade.Sprite(CAMINHO_JOGADOR_uP, scale=ESCALA)
        self.atualizar_posicao_sprite(self.sprites_jogador, self.mundo_jogador_x, self.mundo_jogador_y)



    
       



def executar():
    mundo = Mundo()
    rodando = True
    
    while rodando:
        mundo.renderizar()
        comando = input('\n> ').strip().lower()
        
        if comando == 'w':
            mundo.mover_jogador(0, -1)
        elif comando == 's':
            mundo.mover_jogador(0, 1)  # Movimenta para baixo
        elif comando == 'a':
            mundo.mover_jogador(-1, 0)
        elif comando == 'd':
            mundo.mover_jogador(1, 0)
        elif comando == '1' or comando == 'q':
            rodando = False
            continue
        else: 
            print('Comando inválido!')
            continue 
        
        mundo.vagar_inimigo()
        
    print('Obrigado por jogar!')

if __name__ == '__main__':
    executar()


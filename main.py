import AutomatoFD as AF
from time import time,sleep
import pygame, glob
from pygame.locals import (
    K_w,
    K_r,
    K_d,
    K_a,
    K_s,
    K_c,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 395

afd = AF.AutomatoFD('vadcrwsRS') #instancia o objeto do autômato
afdXml = afd.leXML('automato.jff') #lê o arquivo gerado pelo JFLAP
afd.carregaAFD(afdXml) #define os estados e transições a partir do arquivo lido

#Inicializa a classe
pygame.init()

#Seta o tamanho da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#classe do jogador
class Player:
    def __init__(self):
        super(Player, self).__init__()
        self.ani_speed_init=3
        self.ani_speed=self.ani_speed_init
        #diretorio dos sprites
        self.ani = glob.glob("Sprites_Shikamaru/Stand/sprite_*.png")
        self.ani.sort()
        self.ani_pos=0
        self.ani_max = len(self.ani)-1
        self.image = pygame.image.load(self.ani[0]).convert_alpha()
        #primeira imagem a mostrar na tela
        self.update(0,"Stand/sprite_*.png", 100)

    #cada estado muda o conjunto de sprites para cada acao diferete, dependendo do diretorio mandado
    def update(self, pos, img, speed):
        if pos !=0:
            self.ani_speed-=1
            if self.ani_speed == 0:
                self.ani = glob.glob("Sprites_Shikamaru/" + img)
                self.image = pygame.image.load(self.ani[self.ani_pos]).convert_alpha()
                self.ani_speed = speed
                if self.ani_pos == self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos+=1
        screen.blit(self.image,(240,150))

#imagem de fundo
imp = pygame.image.load("Sprites_Shikamaru/kages3.png").convert_alpha()

#Instaciando a classe player
player = Player()
pos = 1
#diretorio dos sprites
img = "Stand/sprite_*.png"
sped = 3

# roda ate pedir para fechar
running = True
while running:

    #upload da imagem do player
    player.update(pos, img, sped)
    #display a tela a cada frame que mudar
    pygame.display.update()
    #upload da imagem de fundo
    screen.blit(imp, (0, 0))

    cadeia = None

    #a cada tecla pressionada a funcao pega do sistema e coloca na cadeia
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pressed_keys[K_d]:
            cadeia ='d'
        elif pressed_keys[K_a]:
            cadeia ='a'
        elif pressed_keys[K_w]:
            cadeia ='w'
        elif pressed_keys[K_r]:
            cadeia ='r'
            if pressed_keys[K_s]:
                cadeia = cadeia +'s'
        elif pressed_keys[K_s]:
            cadeia ='s'
        elif pressed_keys[K_c]:
            cadeia ='c'

    if cadeia == None:
        pass
    else:
        cadeia = afd.insereV(cadeia) #insere v's na cadeia
        verifica = afd.aceitaCadeia(cadeia) #verifica se a cadeia é aceita ou não

        if (verifica == 0): #se a cadeia for aceita, podemos processar os sprites
            for i in range(len(cadeia)):
                estadoAtual = afd.move(cadeia[i]) #move o automato passo a passo
                img = afd.acaoSprite(estadoAtual)
                if img != None:
                    pos = 1
                    #entra em loop ate terminar de rodar os sprites do especial
                    if estadoAtual == 4:
                        start = time()
                        while(time() - start < 4):
                            player.update(pos, img, 3)
                            pygame.display.update()
                            screen.blit(imp, (0, 0))
                            sleep(0.2)
                else:
                    pos = 0
                #troca a imagem do player
                player.update(pos, img, sped)
                #display a tela a cada frame que mudar
                pygame.display.update()
                #screen.blit(imp, (0, 0))
                screen.blit(imp, (0, 0))
        else: # a cadeia não for aceita, não processa os sprites
            print('rejeita cadeia')

# fecha o jogo
pygame.quit()

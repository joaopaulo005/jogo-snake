import pygame
import random

pygame.init()
pygame.display.set_caption('Jogo Snake Python')
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

tamanho_quadrado = 10
velocidade_jogo = 30

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('Helvetica', 35)
    texto = fonte.render(f'Pontos: {pontuacao}', True, verde)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def tela_game_over(pontuacao):
    tela.fill(preta)
    fonte_grande = pygame.font.SysFont('Helvetica', 72)
    texto_game_over = fonte_grande.render('Game Over', True, vermelha)
    texto_reiniciar = fonte_grande.render('Pressione R para jogar novamente', True, branca)
    texto_sair = fonte_grande.render('Pressione Q para sair', True, branca)
    fonte_pontuacao = pygame.font.SysFont('Helvetica', 48)
    texto_pontuacao = fonte_pontuacao.render(f'Pontuação: {pontuacao}', True, verde)

    tela.blit(texto_game_over, (largura / 2 - texto_game_over.get_width() / 2, altura / 8))
    tela.blit(texto_reiniciar, (largura / 2 - texto_reiniciar.get_width() / 2, altura / 2))
    tela.blit(texto_sair, (largura / 2 - texto_sair.get_width() / 2, altura * 3 / 4))
    tela.blit(texto_pontuacao, (largura / 2 - texto_pontuacao.get_width() / 2, altura / 3))

    pygame.display.update()

    esperando_escolha = True
    while esperando_escolha:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    rodar_jogo()
                    esperando_escolha = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

def rodar_jogo():
    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y

        if [x, y] in pixels[:-1]:
            fim_jogo = True

        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        pygame.display.update()

        relogio.tick(velocidade_jogo)

    tela_game_over(tamanho_cobra - 1)

rodar_jogo()
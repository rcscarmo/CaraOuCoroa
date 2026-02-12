import os
import pygame
import random

def loadMoedaRandom():
    moedas = ['dolar', 'euro', 'real', 'yen']
    escolha = random.choice(moedas)
    return escolha
moeda = loadMoedaRandom()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init() 

# tela
LARGURA, ALTURA = 1024, 768
screen = pygame.display.set_mode((LARGURA, ALTURA))
# screen = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED|pygame.FULLSCREEN)
pygame.display.set_caption("Cara ou Coroa")
clock = pygame.time.Clock()

# imagens
try:
    moeda_frente = pygame.image.load(
        os.path.join("images", "moedas", f"{moeda}_1.png")
    ).convert_alpha()
    moeda_verso = pygame.image.load(
        os.path.join("images", "moedas", f"{moeda}_2.png")
    ).convert_alpha()
except pygame.error as exc:
    raise SystemExit(f"Falha ao carregar imagens da moeda: {exc}") from exc

# som
try:
    som_moeda = pygame.mixer.Sound(os.path.join("sfx", "coin.wav"))
    som_moeda.set_volume(0.5)
except pygame.error as exc:
    raise SystemExit(f"Falha ao carregar som da moeda: {exc}") from exc

# fonte
fonte = pygame.font.SysFont(None, 72)

# estado da moeda
moeda_atual = moeda_frente
centro = (LARGURA // 2, ALTURA // 2)

# animação
girando = False
escala_x = 1.0
velocidade = 0.12
fase = "fechando"  # fechando -> abrindo
resultado = None

# texto fade
alpha_texto = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not girando:
                girando = True
                fase = "fechando"
                escala_x = 1.0
                resultado = random.choice(["CARA", "COROA"])
                alpha_texto = 0

    # animação da moeda
    if girando:
        if fase == "fechando":
            escala_x -= velocidade
            if escala_x <= 0:
                escala_x = 0
                som_moeda.play()
                # troca imagem no meio do giro
                moeda_atual = moeda_frente if resultado == "CARA" else moeda_verso
                fase = "abrindo"
        elif fase == "abrindo":
            escala_x += velocidade
            if escala_x >= 1:
                escala_x = 1
                girando = False

    # fundo
    screen.fill("purple")

    # desenhar moeda
    largura = max(1, int(moeda_atual.get_width() * escala_x))
    altura = moeda_atual.get_height()

    moeda_escalada = pygame.transform.scale(moeda_atual, (largura, altura))
    moeda_rect = moeda_escalada.get_rect(center=centro)
    screen.blit(moeda_escalada, moeda_rect)

    # texto com fade-in
    if not girando and resultado:
        if alpha_texto < 255:
            alpha_texto += 5

        texto = fonte.render(resultado, True, "white")
        texto.set_alpha(alpha_texto)
        texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 + 210))
        screen.blit(texto, texto_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

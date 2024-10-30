import pygame

# Configurações do Pygame
WIDTH, HEIGHT = 300, 300
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
FPS = 1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quebra-Cabeça 8")
font = pygame.font.Font(None, 74)


def draw_board(tabuleiro_str):
    """Desenha o tabuleiro na tela."""
    # Converte a string do tabuleiro para lista
    if isinstance(tabuleiro_str, str):
        tabuleiro = eval(tabuleiro_str)
    else:
        tabuleiro = tabuleiro_str

    screen.fill(BACKGROUND_COLOR)
    tile_size = WIDTH // 3

    for i in range(3):
        for j in range(3):
            value = tabuleiro[i][j]
            if value != 0:  # Não desenha o número 0 (espaço vazio)
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(
                    center=(
                        j * tile_size + tile_size // 2,
                        i * tile_size + tile_size // 2,
                    )
                )
                screen.blit(text, text_rect)
            pygame.draw.rect(
                screen,
                LINE_COLOR,
                (j * tile_size, i * tile_size, tile_size, tile_size),
                2,
            )

    pygame.display.flip()


def move(tab_original):
    movimentos = []
    tab = eval(tab_original)
    i = 0
    j = 0
    while 0 not in tab[i]:
        i += 1
    j = tab[i].index(0)

    # Movimentos possíveis
    if i < 2:  # mover o 0 para baixo
        tab[i][j], tab[i + 1][j] = tab[i + 1][j], tab[i][j]
        movimentos.append(str(tab))
        tab[i][j], tab[i + 1][j] = tab[i + 1][j], tab[i][j]

    if i > 0:  # mover o 0 para cima
        tab[i][j], tab[i - 1][j] = tab[i - 1][j], tab[i][j]
        movimentos.append(str(tab))
        tab[i][j], tab[i - 1][j] = tab[i - 1][j], tab[i][j]

    if j < 2:  # mover o 0 para a direita
        tab[i][j], tab[i][j + 1] = tab[i][j + 1], tab[i][j]
        movimentos.append(str(tab))
        tab[i][j], tab[i][j + 1] = tab[i][j + 1], tab[i][j]

    if j > 0:  # mover o 0 para a esquerda
        tab[i][j], tab[i][j - 1] = tab[i][j - 1], tab[i][j]
        movimentos.append(str(tab))
        tab[i][j], tab[i][j - 1] = tab[i][j - 1], tab[i][j]

    return movimentos


def bfs(start, end):
    explorado = []
    banco = [[start]]
    while banco:
        i = 0
        caminho = banco[i]
        banco = banco[:i] + banco[i + 1 :]
        final = caminho[-1]
        if final in explorado:
            continue
        for movimento in move(final):
            if movimento in explorado:
                continue
            banco.append(caminho + [movimento])
        explorado.append(final)
        if final == end:
            break
    return caminho


def h_misplaced(tabuleiro):
    misplaced = 0
    comparador = 1
    tab = eval(tabuleiro)
    for i in range(0, 3):
        for j in range(0, 3):
            if tab[i][j] != comparador % 9:
                misplaced += 1
            comparador += 1
    return misplaced


def a_estrela(start, end):
    explorado = []
    # Armazenamos o custo separadamente do caminho
    banco = [([h_misplaced(start)], [start])]  # ([custos], [caminho])

    while banco:
        i = 0
        for j in range(1, len(banco)):
            if banco[i][0][0] > banco[j][0][0]:
                i = j

        custos, caminho = banco[i]
        banco = banco[:i] + banco[i + 1 :]
        final = caminho[-1]

        if final in explorado:
            continue

        for movimento in move(final):
            if movimento in explorado:
                continue
            novo_custo = custos[0] + h_misplaced(movimento) + h_misplaced(final)
            banco.append(([novo_custo], caminho + [movimento]))

        explorado.append(final)
        if final == end:
            return caminho  # Retorna apenas o caminho, sem os custos

    return None


# Loop principal do Pygame
def main(caminho):
    if not caminho:
        print("Nenhum caminho encontrado!")
        return

    clock = pygame.time.Clock()
    running = True
    step = 0

    while running and step < len(caminho):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(caminho[step])
        pygame.time.delay(1000)
        step += 1
        clock.tick(FPS)

    # Aguarda alguns segundos no estado final
    if running:
        pygame.time.delay(2000)


if __name__ == "__main__":
    # Tabuleiro inicial e final
    tabuleiro = str([[4, 3, 6], [8, 7, 1], [0, 5, 2]])
    obj_final = str([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    print("Usando Busca em Largura:")
    caminho_bfs = bfs(tabuleiro, obj_final)
    print("Mostrando passos da busca em largura:")
    main(caminho_bfs)

    print("\nUsando A*:")
    caminho_a_estrela = a_estrela(tabuleiro, obj_final)
    print("Mostrando passos da busca A*:")
    main(caminho_a_estrela)

    pygame.quit()

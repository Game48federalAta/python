import chess.pgn
import chess.engine
import time
import pygame
import sys

# Stockfish motorunun yolu (senin indirdiğin exe dosyasının yolu)
STOCKFISH_PATH = r"./stockfish/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TILE_SIZE = 64
ROW, COL = 8, 8

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)

run = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()
FPS = 60
move_index = 0

text_font = pygame.font.SysFont("Aria", 24)

def scale(img):
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return img

pieces = {
    "P": scale(pygame.image.load("alpha/wP.png").convert_alpha()),  # beyaz piyon
    "N": scale(pygame.image.load("alpha/wN.png").convert_alpha()),  # beyaz at
    "B": scale(pygame.image.load("alpha/wB.png").convert_alpha()),  # beyaz fil
    "R": scale(pygame.image.load("alpha/wR.png").convert_alpha()),  # beyaz kale
    "Q": scale(pygame.image.load("alpha/wQ.png").convert_alpha()),  # beyaz vezir
    "K": scale(pygame.image.load("alpha/wK.png").convert_alpha()),  # beyaz şah
    "p": scale(pygame.image.load("alpha/bP.png").convert_alpha()),  # siyah piyon
    "n": scale(pygame.image.load("alpha/bN.png").convert_alpha()),  # siyah at
    "b": scale(pygame.image.load("alpha/bB.png").convert_alpha()),  # siyah fil
    "r": scale(pygame.image.load("alpha/bR.png").convert_alpha()),  # siyah kale
    "q": scale(pygame.image.load("alpha/bQ.png").convert_alpha()),  # siyah vezir
    "k": scale(pygame.image.load("alpha/bK.png").convert_alpha()),  # siyah şah
}

back_bttn_img = pygame.image.load("button/back.png").convert_alpha()
next_bttn_img = pygame.image.load("button/next.png").convert_alpha()
stop_bttn_img = pygame.image.load("button/pause.png").convert_alpha()
play_bttn_img = pygame.image.load("button/play.png").convert_alpha()
show_first_move_bttn_img = pygame.image.load("button/start.png").convert_alpha()
show_last_move_bttn_img = pygame.image.load("button/last.png").convert_alpha()

class Button:
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def draw_game_info():
    white_text = text_font.render(f"{white_player[0]}({white_player[1]})", True, (0, 0, 0))
    black_text = text_font.render(f"{black_player[0]}({black_player[1]})", True, (0, 0, 0))
    screen.blit(white_text, (16, 0))  # Beyaz üstte (orijinal koduna göre)
    screen.blit(black_text, (16, (TILE_SIZE * 8) + 16))  # Siyah altta

def draw_bg():
    screen.fill(WHITE)
    for row in range(ROW):
        for col in range(COL):
            if (row + col) % 2 == 1:  # Siyah kareleri belirle
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (16 + col * TILE_SIZE, 16 + row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )

def draw_board():
    for i in range(8):
        rank = i  # Orijinal koduna göre beyaz üstte (rank 0 üstte beyaz)
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            if piece:
                symbol = piece.symbol()
                screen.blit(pieces[symbol], (16 + file * TILE_SIZE, 16 + i * TILE_SIZE))

def go_to_move(index):
    global move_index
    move_index = max(0, min(len(all_moves), index))
    board.reset()
    for i in range(move_index):
        board.push(all_moves[i])

# PGN dosyası aç
with open("game2.pgn") as pgn:
    game = chess.pgn.read_game(pgn)

white_player = (game.headers.get("White"), game.headers.get("WhiteElo"))
black_player = (game.headers.get("Black"), game.headers.get("BlackElo"))

back_button = Button(600, 450, back_bttn_img, 0.2)
next_button = Button(700, 450, next_bttn_img, 0.2)
play_button = Button(650, 450, play_bttn_img, 0.2)
first_button = Button(550, 450, show_first_move_bttn_img, 0.2)
last_button = Button(750, 450, show_last_move_bttn_img, 0.2)

board = game.board()
all_moves = list(game.mainline_moves())

# Motoru başlat (kullanılmıyorsa kaldırılabilir)
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH, setpgrp=True)
engine.configure({"Threads": 2})

is_playing = False

last_move_time = 0
move_delay = 500  # 0.5 saniye

while run:
    clock.tick(FPS)

    draw_bg()
    draw_board()

    # Butonları çiz (eylemsiz)
    back_button.draw(screen)
    next_button.draw(screen)
    play_button.draw(screen)
    first_button.draw(screen)
    last_button.draw(screen)

    draw_game_info()

    # Otomatik oynatma
    current_time = pygame.time.get_ticks()
    if is_playing and move_index < len(all_moves):
        if current_time - last_move_time >= move_delay:
            go_to_move(move_index + 1)
            last_move_time = current_time

    # Eventler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if back_button.rect.collidepoint(pos):
                go_to_move(move_index - 1)
            elif next_button.rect.collidepoint(pos):
                go_to_move(move_index + 1)
            elif first_button.rect.collidepoint(pos):
                go_to_move(0)
            elif last_button.rect.collidepoint(pos):
                go_to_move(len(all_moves))
            elif play_button.rect.collidepoint(pos):
                is_playing = not is_playing
                if is_playing:
                    play_button.image = pygame.transform.scale(stop_bttn_img, (int(stop_bttn_img.get_width() * 0.2), int(stop_bttn_img.get_height() * 0.2)))
                else:
                    play_button.image = pygame.transform.scale(play_bttn_img, (int(play_bttn_img.get_width() * 0.2), int(play_bttn_img.get_height() * 0.2)))

    pygame.display.flip()

engine.quit()


# Euphoria
#Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria Euphoria 
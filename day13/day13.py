from enum import unique, IntEnum
from intcode import IntcodeComputer
import pygame
from pygame.locals import *
import sys

FPS = 60
TILE_SIZE = 20
TILES_X = 38
TILES_Y = 21

TITLE = "Advent of Code - Day 13: Care Package"

@unique
class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

COLORS = [
    (0xF1, 0xF7, 0xED),
    (0x54, 0x49, 0x4B),
    (0xE3, 0xD0, 0x81),
    (0x91, 0xC7, 0xB1),
    (0xB3, 0x39, 0x51)
]

def drawBoard(board, screen):
    screen.fill((0, 0, 0))
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.fill(COLORS[value], rect)

    pygame.display.flip()

def day13(filename):
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * TILES_X, TILE_SIZE * TILES_Y), 0, 32)
    pygame.display.set_caption(TITLE)

    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    computer = IntcodeComputer(program)
    my_clock = pygame.time.Clock()
    board = [[0 for _ in range(TILES_X)] for _ in range(TILES_Y)]

    while not computer.finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        my_clock.tick(FPS)

        computer.run()
        for x, y, tile_id in zip(*[computer] * 3):
            if x == -1 and y == 0:
                pygame.display.set_caption(f"{TITLE}    SCORE: {tile_id}")
            else:
                board[y][x] = tile_id

                if tile_id == Tile.BALL:
                    ball_x = x
                elif tile_id == Tile.PADDLE:
                    paddle_x = x

        computer.send(1 if ball_x > paddle_x else -1 if ball_x < paddle_x else 0)
        drawBoard(board, screen)

if __name__ == "__main__":
    try:
        day13(sys.argv[1])
        while pygame.event.poll().type != QUIT:
            pass
        pygame.quit()
    except Exception:
        pygame.quit()
        raise

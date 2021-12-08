import pygame
from random import randint, random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        s = set()
        k = 0
        while len(s) < 300:
            s.add(randint(0, 2303))
        for n, i in enumerate(self.board):
            for m, j in enumerate(i):
                if k in s:
                    if random() < 0.5:
                        self.board[n][m] = 1
                    else:
                        self.board[n][m] = 4
                k += 1
        self.board[0][0] = 2
        self.board[35][63] = 3
        self.f, self.s = [0, 0], [35, 63]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        # 0 - ничего, 1 - стена, 2 - первый игрок, 3 - второй игрок, 4 - вода

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:
                    screen.fill("#964b00", pygame.Rect(x, y, self.cell_size, self.cell_size))
                elif self.board[i][j] == 2:
                    pygame.draw.circle(screen, "purple", (x + self.cell_size * 0.5, y + self.cell_size * 0.5),
                                       self.cell_size * 0.5 - 4)
                elif self.board[i][j] == 3:
                    pygame.draw.circle(screen, "red", (x + self.cell_size * 0.5, y + self.cell_size * 0.5),
                                       self.cell_size * 0.5 - 4)
                elif self.board[i][j] == 4:
                    screen.fill("blue", pygame.Rect(x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, "white", (x, y, self.cell_size, self.cell_size), 1)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def on_click(self, cell_coords):
        pass

    def get_cell(self, mouse_pos):
        y, x = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
        if not (-1 < x < self.height and -1 < y < self.width):
            return None
        return x, y

    def up1(self):
        x, y = self.f
        if x > 0 and self.board[x - 1][y] == 0:
            self.board[x][y] = 0
            self.f[0] -= 1
            self.board[self.f[0]][y] = 2

    def right1(self):
        x, y = self.f
        if y < 63 and self.board[x][y + 1] == 0:
            self.board[x][y] = 0
            self.f[1] += 1
            self.board[x][y + 1] = 2

    def down1(self):
        x, y = self.f
        if x < 35 and self.board[x + 1][y] == 0:
            self.board[x][y] = 0
            self.f[0] += 1
            self.board[self.f[0]][y] = 2

    def left1(self):
        x, y = self.f
        if y > 0 and self.board[x][y - 1] == 0:
            self.board[x][y] = 0
            self.f[1] -= 1
            self.board[x][y - 1] = 2

    def up2(self):
        x, y = self.s
        if x > 0 and self.board[x - 1][y] == 0:
            self.board[x][y] = 0
            self.s[0] -= 1
            self.board[self.s[0]][y] = 3

    def right2(self):
        x, y = self.s
        if y < 63 and self.board[x][y + 1] == 0:
            self.board[x][y] = 0
            self.s[1] += 1
            self.board[x][y + 1] = 3

    def down2(self):
        x, y = self.s
        if x < 35 and self.board[x + 1][y] == 0:
            self.board[x][y] = 0
            self.s[0] += 1
            self.board[self.s[0]][y] = 3

    def left2(self):
        x, y = self.s
        if y > 0 and self.board[x][y - 1] == 0:
            self.board[x][y] = 0
            self.s[1] -= 1
            self.board[x][y - 1] = 3


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
board = Board(64, 36)
board.set_view(0, 0, 30)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                board.up1()
            if event.key == pygame.K_d:
                board.right1()
            if event.key == pygame.K_s:
                board.down1()
            if event.key == pygame.K_a:
                board.left1()
            if event.key == pygame.K_UP:
                board.up2()
            if event.key == pygame.K_RIGHT:
                board.right2()
            if event.key == pygame.K_DOWN:
                board.down2()
            if event.key == pygame.K_LEFT:
                board.left2()
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()

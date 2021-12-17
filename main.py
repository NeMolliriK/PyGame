import pygame
from random import randint, random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 50
        self.board = [[0] * self.width for _ in range(self.height)]
        self.top = 15
        self.left = 10
        s = set()
        k = 0
        while len(s) < 199:
            s.add(randint(0, WIDTH * HEIGHT - 1))
        for n, i in enumerate(self.board):
            for m, j in enumerate(i):
                if k in s and (n != 0 or m != 0) and (n != HEIGHT - 1 or m != WIDTH - 1):
                    if random() < 0.5:
                        self.board[n][m] = 1
                        Wall(walls, x=self.left + self.cell_size * m, y=self.top + self.cell_size * n, file="wall.png")
                    else:
                        self.board[n][m] = 4
                        Puddle(water, x=self.left + self.cell_size * m, y=self.top + self.cell_size * n,
                               file="puddle.png")
                k += 1
        self.board[0][0] = 2
        self.board[HEIGHT - 1][WIDTH - 1] = 3
        self.f, self.s = [0, 0], [HEIGHT - 1, WIDTH - 1]
        walls.draw(screen)
        # 0 - ничего, 1 - стена, 2 - первый игрок, 3 - второй игрок, 4 - вода

    def render(self):
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    first_player.update(x, y)
                elif self.board[i][j] == 3:
                    second_player.update(x, y)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(*cell)

    def on_click(self, n, m):
        pass

    def get_cell(self, mouse_pos):
        y, x = self.left + mouse_pos[0] // self.cell_size, self.top + mouse_pos[1] // self.cell_size
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
        if y < WIDTH - 1 and self.board[x][y + 1] == 0:
            self.board[x][y] = 0
            self.f[1] += 1
            self.board[x][y + 1] = 2
        if first_player.direction == 0:
            first_player.flip()

    def down1(self):
        x, y = self.f
        if x < HEIGHT - 1 and self.board[x + 1][y] == 0:
            self.board[x][y] = 0
            self.f[0] += 1
            self.board[self.f[0]][y] = 2

    def left1(self):
        x, y = self.f
        if y > 0 and self.board[x][y - 1] == 0:
            self.board[x][y] = 0
            self.f[1] -= 1
            self.board[x][y - 1] = 2
        if first_player.direction:
            first_player.flip()

    def up2(self):
        x, y = self.s
        if x > 0 and self.board[x - 1][y] == 0:
            self.board[x][y] = 0
            self.s[0] -= 1
            self.board[self.s[0]][y] = 3

    def right2(self):
        x, y = self.s
        if y < WIDTH - 1 and self.board[x][y + 1] == 0:
            self.board[x][y] = 0
            self.s[1] += 1
            self.board[x][y + 1] = 3
        if second_player.direction == 0:
            second_player.flip()

    def down2(self):
        x, y = self.s
        if x < HEIGHT - 1 and self.board[x + 1][y] == 0:
            self.board[x][y] = 0
            self.s[0] += 1
            self.board[self.s[0]][y] = 3

    def left2(self):
        x, y = self.s
        if y > 0 and self.board[x][y - 1] == 0:
            self.board[x][y] = 0
            self.s[1] -= 1
            self.board[x][y - 1] = 3
        if second_player.direction:
            second_player.flip()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group, x=0, y=0, file="texture.png"):
        super().__init__(*group)
        self.image = pygame.image.load(f"data/{file}")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)


class Player(Sprite):
    def __init__(self, *group, x=0, y=0, file="texture.png"):
        super().__init__(*group, x=x, y=y, file=file)
        self.direction = 1

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.direction = 0 if self.direction else 1

    def die(self):
        self.kill()


class Wall(Sprite):
    pass


class Puddle(Sprite):
    pass


class Bullet(Sprite):
    def __init__(self, *group, x=0, y=0, file="texture.png", direction=None, enemy=None):
        super().__init__(*group, x=x, y=y, file=file)
        self.direction = direction
        if direction == 0 or direction == 2:
            self.image = pygame.transform.rotate(self.image, 90)
        self.enemy = enemy

    def update(self):
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
        elif pygame.sprite.spritecollideany(self, self.enemy):
            pygame.sprite.spritecollideany(self, self.enemy).die()
            self.kill()
        else:
            if self.direction == 0:
                self.rect.y -= 1
            elif self.direction == 1:
                self.rect.x += 1
            elif self.direction == 2:
                self.rect.y += 1
            elif self.direction == 3:
                self.rect.x -= 1


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
walls = pygame.sprite.Group()
first_players = pygame.sprite.Group()
second_players = pygame.sprite.Group()
water = pygame.sprite.Group()
bullets = pygame.sprite.Group()
WIDTH, HEIGHT = 38, 21
board = Board(WIDTH, HEIGHT)
running = True
first_player = Player(first_players, x=10, y=15, file="first_player.png")
second_player = Player(second_players, x=1860, y=1015, file="second_player.png")
second_player.flip()
background = pygame.image.load("data/background.png")
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
            if event.key == pygame.K_t:
                Bullet(bullets, x=first_player.rect.x + 20, y=first_player.rect.y - 30, file="bullet.png", direction=0,
                       enemy=second_players)
            if event.key == pygame.K_h:
                Bullet(bullets, x=first_player.rect.x + 50, y=first_player.rect.y + 20, file="bullet.png", direction=1,
                       enemy=second_players)
            if event.key == pygame.K_g:
                Bullet(bullets, x=first_player.rect.x + 20, y=first_player.rect.y + 50, file="bullet.png", direction=2,
                       enemy=second_players)
            if event.key == pygame.K_f:
                Bullet(bullets, x=first_player.rect.x - 30, y=first_player.rect.y + 20, file="bullet.png", direction=3,
                       enemy=second_players)
            if event.key == pygame.K_KP5:
                Bullet(bullets, x=second_player.rect.x + 20, y=second_player.rect.y - 30, file="bullet.png",
                       direction=0, enemy=first_players)
            if event.key == pygame.K_KP3:
                Bullet(bullets, x=second_player.rect.x + 50, y=second_player.rect.y + 20, file="bullet.png",
                       direction=1, enemy=first_players)
            if event.key == pygame.K_KP2:
                Bullet(bullets, x=second_player.rect.x + 20, y=second_player.rect.y + 50, file="bullet.png",
                       direction=2, enemy=first_players)
            if event.key == pygame.K_KP1:
                Bullet(bullets, x=second_player.rect.x - 30, y=second_player.rect.y + 20, file="bullet.png",
                       direction=3, enemy=first_players)
    screen.blit(background, (0, 0))
    board.render()
    first_players.draw(screen)
    second_players.draw(screen)
    walls.draw(screen)
    water.draw(screen)
    bullets.update()
    bullets.draw(screen)
    pygame.display.flip()

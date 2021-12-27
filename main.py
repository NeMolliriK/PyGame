import pygame
from random import choice, randint
import datetime as dt
import pymorphy2
from maps import MAPS
import sys


class Board:
    def __init__(self, width, height):
        global FS, SS
        self.width = width
        self.height = height
        self.cell_size = 50
        self.board = [[0] * self.width for _ in range(self.height)]
        self.top = (1080 - (HEIGHT * self.cell_size + self.cell_size)) // 2
        self.left = (1920 - WIDTH * self.cell_size) // 2
        self.board = MAP[0]
        FS = MAP[1]  # скорость пули
        SS = MAP[1]
        for n, i in enumerate(self.board):
            for m, j in enumerate(i):
                if j == 1:
                    Wall(walls, x=self.left + self.cell_size * m, y=self.top + self.cell_size * n, file="wall.png")
                elif j == 4:
                    Puddle(water, x=self.left + self.cell_size * m, y=self.top + self.cell_size * n, file="puddle.png")
        self.board[0][0] = 2
        self.board[HEIGHT - 1][WIDTH - 1] = 3
        self.f, self.s = [0, 0], [HEIGHT - 1, WIDTH - 1]
        walls.draw(screen)
        # 0 - ничего, 1 - стена, 2 - первый игрок, 3 - второй игрок, 4 - вода

    def render(self):
        global first_suffocates, second_suffocates, draw
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
        if pygame.sprite.spritecollideany(first_player,
                                          gases) and not first_suffocates and pygame.sprite.spritecollideany(
                second_player,
                gases) and not second_suffocates and not draw and first_player.lives == second_player.lives:
            draw = 1
        elif not pygame.sprite.spritecollideany(first_player,
                                                gases) and first_suffocates and not pygame.sprite.spritecollideany(
                second_player, gases) and second_suffocates and draw or first_player.lives != second_player.lives:
            draw = 0
        if pygame.sprite.spritecollideany(first_player, gases):
            if not first_suffocates:
                pygame.time.set_timer(poisoning_of_first, 1000)
                first_suffocates = 1
        else:
            if first_suffocates:
                pygame.time.set_timer(poisoning_of_first, 0)
                first_suffocates = 0
        if pygame.sprite.spritecollideany(second_player, gases):
            if not second_suffocates:
                pygame.time.set_timer(poisoning_of_second, 1000)
                second_suffocates = 1
        else:
            if second_suffocates:
                pygame.time.set_timer(poisoning_of_second, 0)
                second_suffocates = 0

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

    def narrowing_of_zone(self):
        for n in range(HEIGHT):
            for m in range(WIDTH):
                if n == z or n == HEIGHT - 1 - z or m == z or m == WIDTH - 1 - z:
                    Vapors(gases, x=self.left + self.cell_size * m, y=self.top + self.cell_size * n,
                           file="poisonous_vapors.png")


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group, x=100, y=100, file="texture.png"):
        super().__init__(*group, all_sprites)
        self.image = pygame.image.load(f"data/{file}")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)


class Player(Sprite):
    def __init__(self, *group, x=100, y=100, file="texture.png", lives=5, nick="Player"):
        super().__init__(*group, x=x, y=y, file=file)
        all_sprites.remove(self)
        self.direction = 1
        self.file = file
        self.a = 1
        self.lives = lives
        if group[0] == first_players:
            x = board.left
            for i in range(lives):
                Heart(first_hearts, x=x, y=board.top + board.height * board.cell_size + 10, file="heart.png")
                x += board.cell_size + 5
        else:
            x = 1920 - board.left - board.cell_size
            for i in range(lives):
                Heart(second_hearts, x=x, y=board.top + board.height * board.cell_size + 10, file="heart.png")
                x -= board.cell_size + 5
        self.nick = nick

    def update(self, x, y):
        if self.a:
            self.rect.x, self.rect.y = x, y

    def flip(self):
        if self.a:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = 0 if self.direction else 1

    def damage(self, d):
        self.lives -= d
        if first_players.has(self):
            try:
                for i in range(d):
                    first_hearts.sprites()[-1].kill()
            except IndexError:
                first_hearts.empty()
        else:
            try:
                for i in range(d):
                    second_hearts.sprites()[-1].kill()
            except IndexError:
                second_hearts.empty()
        damage.play()
        if self.lives < 1:
            self.die()

    def die(self):
        global a, intro_text_1, intro_text_2, draw, intro_text_3, intro_text_4
        if self.a:
            pygame.mixer.music.stop()
            self.image = pygame.image.load(f"data/dead_{self.file}")
            file = open("victories.txt", "a")
            word = morph.parse('секунда')[0]
            word2 = morph.parse('выстрел')[0]
            t = self.nick == sn
            if not draw:
                death.play()
                intro_text_1 = f"{fn if t else sn} победил {self.nick} за {(pygame.time.get_ticks() - ticks) / 1000} " \
                               f"{word.make_agree_with_number((pygame.time.get_ticks() - ticks) // 1000).word} и "
                intro_text_2 = f"{fshots if t else sshots} " \
                               f"{word2.make_agree_with_number(fshots if t else sshots).word} в " \
                               f"{dt.datetime.now().time().isoformat(timespec='minutes')}.\n"
                file.write(intro_text_1 + intro_text_2)
            elif draw == 1:
                simultaneous_death.play()
                intro_text_1 = f"Ничья. Оба игрока одновременно "
                intro_text_2 = f"умерли от зоны в {dt.datetime.now().time().isoformat(timespec='minutes')}. "
                intro_text_3 = f"Всего было произведено {fshots + sshots} " \
                               f"{word2.make_agree_with_number(fshots + sshots).word}"
                intro_text_4 = f"в течение {(pygame.time.get_ticks() - ticks) / 1000} " \
                               f"{word.make_agree_with_number((pygame.time.get_ticks() - ticks) // 1000).word}.\n"
                draw = 2
                file.write(intro_text_1 + intro_text_2 + intro_text_3 + intro_text_4)
            file.close()
            self.a = 0
            a = 0


class Wall(Sprite):
    pass


class Puddle(Sprite):
    pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group, x=100, y=100, file=None, direction=None, enemy=None, speed=5, damage=1, w=30):
        global fshots, sshots
        super().__init__(*group, all_sprites)
        shot.play()
        if enemy == second_players:
            fshots += 1
        else:
            sshots += 1
        if file is None:
            self.image = pygame.Surface((w, 10), pygame.SRCALPHA, 32)
            self.image.fill("grey")
        else:
            self.image = pygame.image.load(f"data/{file}")
            self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if direction == 0 or direction == 2:
            self.image = pygame.transform.rotate(self.image, 90)
        self.enemy = enemy
        self.speed = speed
        self.damage = damage

    def update(self):
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
        elif pygame.sprite.spritecollideany(self, self.enemy):
            pygame.sprite.spritecollideany(self, self.enemy).damage(self.damage)
            self.kill()
        else:
            if self.direction == 0:
                self.rect.y -= self.speed
            elif self.direction == 1:
                self.rect.x += self.speed
            elif self.direction == 2:
                self.rect.y += self.speed
            elif self.direction == 3:
                self.rect.x -= self.speed


class Heart(Sprite):
    pass


def terminate():
    pygame.quit()
    sys.exit()


class Particle(pygame.sprite.Sprite):
    fire = [pygame.image.load("data/star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


class Vapors(Sprite):
    def __init__(self, *group, x=100, y=100, file="texture.png"):
        super().__init__(*group, x=x, y=y, file=file)
        self.image.set_colorkey(self.image.get_at((0, 0)))


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.mixer.music.load("data/lobby.mp3")
pygame.mixer.music.play(-1)
intro_text = ["Управление:", "WASD - передвижение первого игрока", "IJKL - стрельба первого игрока",
              "Стрелки - передвижение второго игрока", "5123 на нумпаде - стрельба второго игрока",
              "Цель - убить своего оппонента", "Для продолжения:", "нажмите 1 для лёгкого уровня", "2 для среднего",
              "и 3 для сложного"]
fon = pygame.transform.scale(pygame.image.load('data/background.png'), (1920, 1080))
screen.blit(fon, (0, 0))
font = pygame.font.Font(None, 100)
text_coord = 150
for line in intro_text:
    string_rendered = font.render(line, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.x = 230
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                walls = pygame.sprite.Group()
                first_players = pygame.sprite.Group()
                second_players = pygame.sprite.Group()
                water = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                first_hearts = pygame.sprite.Group()
                second_hearts = pygame.sprite.Group()
                stars = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                gases = pygame.sprite.Group()
                GRAVITY = 1
                morph = pymorphy2.MorphAnalyzer()
                fshots = 0
                sshots = 0
                if event.key == pygame.K_1:
                    MAP = MAPS[2]
                elif event.key == pygame.K_2:
                    MAP = MAPS[1]
                else:
                    MAP = MAPS[0]
                WIDTH, HEIGHT = len(MAP[0][0]), len(MAP[0])
                board = Board(WIDTH, HEIGHT)
                screen_rect = (0, 0, 1920, 1080)
                fl = 3  # жизни
                sl = 3
                fn = "Player 1"  # ники
                sn = "Player 2"
                first_player = Player(first_players, x=board.left, y=board.top, file="first_player.png", lives=fl,
                                      nick=fn)
                second_player = Player(second_players, x=1920 - 20 + board.left - board.cell_size,
                                       y=1080 - 30 + board.top - board.cell_size, file="second_player.png", lives=sl,
                                       nick=sn)
                second_player.flip()
                background = pygame.image.load("data/background.png")
                first_reload = pygame.USEREVENT + 1
                second_reload = pygame.USEREVENT + 2
                r1 = 1
                r2 = 1
                tr1 = 500  # время перезарядки
                tr2 = 500
                fd = 1  # урон игроков
                sd = 1
                fw = 30  # длина пули
                sw = 30
                zone_damage = 1
                a = 1
                first_suffocates = 0
                second_suffocates = 0
                ticks = pygame.time.get_ticks()
                shot = pygame.mixer.Sound("data/shot.wav")
                damage = pygame.mixer.Sound("data/damage.wav")
                death = pygame.mixer.Sound("data/death.wav")
                simultaneous_death = pygame.mixer.Sound("data/draw.wav")
                pygame.mixer.music.load("data/fight.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.25)
                zone = pygame.USEREVENT + 3
                poisoning_of_first = pygame.USEREVENT + 4
                poisoning_of_second = pygame.USEREVENT + 5
                pygame.time.set_timer(zone, 10000)
                z = 0
                draw = 0
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
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
                            if first_player.a and r1:
                                if event.key == pygame.K_i:
                                    Bullet(bullets, x=first_player.rect.x + 20, y=first_player.rect.y - 30, w=fw,
                                           direction=0, enemy=second_players, speed=FS, damage=fd)
                                    r1 = 0
                                    pygame.time.set_timer(first_reload, tr1)
                                if event.key == pygame.K_l:
                                    Bullet(bullets, x=first_player.rect.x + 50, y=first_player.rect.y + 20, w=fw,
                                           direction=1, enemy=second_players, speed=FS, damage=fd)
                                    r1 = 0
                                    pygame.time.set_timer(first_reload, tr1)
                                if event.key == pygame.K_k:
                                    Bullet(bullets, x=first_player.rect.x + 20, y=first_player.rect.y + 50, w=fw,
                                           direction=2, enemy=second_players, speed=FS, damage=fd)
                                    r1 = 0
                                    pygame.time.set_timer(first_reload, tr1)
                                if event.key == pygame.K_j:
                                    Bullet(bullets, x=first_player.rect.x - 30, y=first_player.rect.y + 20, w=fw,
                                           direction=3, enemy=second_players, speed=FS, damage=fd)
                                    r1 = 0
                                    pygame.time.set_timer(first_reload, tr1)
                            if second_player.a and r2:
                                if event.key == pygame.K_KP5:
                                    Bullet(bullets, x=second_player.rect.x + 20, y=second_player.rect.y - 30, w=sw,
                                           direction=0, enemy=first_players, speed=SS, damage=sd)
                                    r2 = 0
                                    pygame.time.set_timer(second_reload, tr2)
                                if event.key == pygame.K_KP3:
                                    Bullet(bullets, x=second_player.rect.x + 50, y=second_player.rect.y + 20, w=sw,
                                           direction=1, enemy=first_players, speed=SS, damage=sd)
                                    r2 = 0
                                    pygame.time.set_timer(second_reload, tr2)
                                if event.key == pygame.K_KP2:
                                    Bullet(bullets, x=second_player.rect.x + 20, y=second_player.rect.y + 50, w=sw,
                                           direction=2, enemy=first_players, speed=SS, damage=sd)
                                    r2 = 0
                                    pygame.time.set_timer(second_reload, tr2)
                                if event.key == pygame.K_KP1:
                                    Bullet(bullets, x=second_player.rect.x - 30, y=second_player.rect.y + 20, w=sw,
                                           direction=3, enemy=first_players, speed=SS, damage=sd)
                                    r2 = 0
                                    pygame.time.set_timer(second_reload, tr2)
                        if event.type == first_reload:
                            r1 = 1
                            pygame.time.set_timer(first_reload, 0)
                        if event.type == second_reload:
                            r2 = 1
                            pygame.time.set_timer(second_reload, 0)
                        if event.type == zone:
                            board.narrowing_of_zone()
                            z += 1
                        if event.type == poisoning_of_first:
                            first_player.damage(zone_damage)
                        if event.type == poisoning_of_second:
                            second_player.damage(zone_damage)
                    screen.blit(background, (0, 0))
                    board.render()
                    first_players.draw(screen)
                    second_players.draw(screen)
                    all_sprites.update()
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    if not a:
                        if not draw:
                            pygame.time.wait(2100)
                            intro_text = ["                           ПОБЕДА!!!", intro_text_1, intro_text_2[:-1]]
                            pygame.mixer.music.load("data/victory.mp3")
                        else:
                            pygame.time.wait(2400)
                            intro_text = ["                           НИЧЬЯ!!!", intro_text_1, intro_text_2,
                                          intro_text_3, intro_text_4[:-1]]
                            pygame.mixer.music.load("data/draw.mp3")
                        pygame.mixer.music.play(-1)
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and \
                                        event.key == pygame.K_ESCAPE:
                                    terminate()
                            screen.fill("black")
                            fon = pygame.transform.scale(pygame.image.load('data/background.png'), (1920, 1080))
                            screen.blit(fon, (0, 0))
                            font = pygame.font.Font(None, 100)
                            text_coord = 270
                            for line in intro_text:
                                string_rendered = font.render(line, 1, pygame.Color('white'))
                                intro_rect = string_rendered.get_rect()
                                text_coord += 10
                                intro_rect.top = text_coord
                                intro_rect.x = 260
                                text_coord += intro_rect.height
                                screen.blit(string_rendered, intro_rect)
                            create_particles((randint(0, 1920), randint(0, 1080)))
                            stars.update()
                            stars.draw(screen)
                            pygame.display.flip()
    pygame.display.flip()

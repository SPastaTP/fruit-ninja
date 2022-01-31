import pygame
import sys
import os
import random
import time
import datetime
import schedule
import sqlite3


connect1 = sqlite3.connect('films_db.sqlite')
cursor1 = connect1.cursor()
connect = sqlite3.connect('data.sqlite')
cursor = connect.cursor()
all_sprites = pygame.sprite.Group()
FPS = 50
PRICE = {'Red_Apple.png': 1, 'Coconut.png': 1, 'melon.png': 1, 'Mango.png': 1, 'Pineapple.png': 1,
         'Watermelon.png': 1, 'Banana.png': 1, 'Kiwi.png': 1, 'Lemon.png': 1,
         'Orange.png': 1, 'Pear.png': 1}
NAME_CHANGE = {'Red_Apple.png': ['apple12.png', 'apple2.png'], 'Coconut.png': ['coco1.png', 'coc2.png'],
               'melon.png': ['melon1.png', 'melon2.png'], 'Mango.png': ['mango1.png', 'mango2.png'],
               'Pineapple.png': ['pn1.png', 'pn2.png'],
               'Watermelon.png': ['watermelon1.png', 'watermelon2.png'], 'Banana.png': ['banana1.png', 'banana2.png'],
               'Kiwi.png': ['kiwi1.png', 'kiwi2.png'], 'Lemon.png': ['lemon1.png', 'lemon2.png'],
               'Orange.png': ['or1.png', 'or2.png'], 'Pear.png': ['pear1.png', 'pear2.png']}

data = ['Red_Apple.png', 'Coconut.png', 'Mango.png', 'Pineapple.png', 'Bomb.png', 'Score_2x_Banana.png',
        '5seconds_Banana.png',
        'Watermelon.png', 'Banana.png', 'Kiwi.png', 'Lemon.png', 'Orange.png', 'Pear.png', 'melon.png']

global score
score = 0


def load_image(name, colorkey=None):  # Обработка изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def write_text(sc, text, size, x, y):  # функции для вывода текста
    font = pygame.font.SysFont('bahnschrift', size)
    rendered = font.render(text, True, (255, 255, 255))
    rect = rendered.get_rect()
    rect.midtop = (x, y)
    screen.blit(rendered, rect)


run = False


class Profile:
    pass


class Settings:  # настройки, вызываются клавишей esc (или нажатием на иконку)

    def button(self, color, x, y, width, height, screen, text=None,
               outline=None):  # добавление кнопки на экран(outliтe - цвет контура кнопки)
        if outline:
            pygame.draw.rect(screen, outline, (x - 2, y - 2, width + 4, height + 4), 0)

        pygame.draw.rect(screen, color, (x, y, width, height), 0)

        if text:
            font = pygame.font.SysFont('bahnschrift', 20)
            text = font.render(text, 10, (0, 0, 0))
            screen.blit(text, (
                x + (width / 2 - text.get_width() / 2), y + (height / 2 - text.get_height() / 2)))

    def draw_set(self):
        fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        self.button('white', 370, 232, 500, 70, screen, 'Хочу войти в свой аккаунт', 'black')
        self.button('light grey', 370, 337, 500, 70, screen, 'Остаться в игре с текущим анонимном состоянии', 'black')
        self.button('grey', 370, 442, 500, 70, screen, 'Поменять на темную тему [dangerous!]', 'black')
        self.button('dark grey', 470, 547, 300, 50, screen, 'Вернуться на главное меню', 'black')
        sp_pos_buttons = [(range(370, 870), range(232, 302)), (range(370, 870), range(337, 407)),
                          (range(370, 870), range(442, 512)), (range(470, 770), range(547, 597))]
        while True:
            action = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(sp_pos_buttons)):
                        if event.pos[0] in sp_pos_buttons[i][0] and event.pos[1] in sp_pos_buttons[i][1]:
                            action = i
                            return action
            pygame.display.flip()


class Menu:
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.draw()

    def dict(self, x, y):
        chenge_mode = {'Режим: Zen Mode': (range(69, 389), range(203, 530)),
                       'Режим: Classic Mode': (range(494, 785), range(180, 477)),
                       'Режим: Arcade Mode': (range(891, 1205), range(202, 523)),
                       'Icon': (range(891, 1205), range(202, 523))}
        for el in chenge_mode:
            if x in chenge_mode[el][0] and y in chenge_mode[el][1] and el != 'Icon':
                return True, el
        return False, ''

    def draw(self):
        cursor_flag = False
        text = ''
        global run, scene
        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        cursor_group = pygame.sprite.Group()
        cur_image = load_image('arrow.png')
        cursor = pygame.sprite.Sprite(cursor_group)
        cursor.image = cur_image
        cursor.rect = cursor.image.get_rect()
        pygame.mouse.set_visible(True)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION:
                    cursor.rect.x = event.pos[0]
                    cursor.rect.y = event.pos[1]
                    cursor_flag, text = self.dict(cursor.rect.x, cursor.rect.y)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run, scene1 = self.dict(event.pos[0], event.pos[1])
                    if run:
                        global scenes
                        scene = scenes[scene1[7:]]

                        global start_time, extra_time
                        start_time = time.time()
                        extra_time = 0
                        return scenes[scene1[7:]]
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        set = Settings()
                        action = set.draw_set()
                        if action == 0:
                            pass
                # переход в настройки
            screen.blit(fon, (0, 0))
            if cursor_flag:
                pygame.mouse.set_visible(False)
                cursor_group.draw(screen)
                write_text(screen, text, 50, 650, 550)
            else:
                pygame.mouse.set_visible(True)
            pygame.display.flip()


class Sprites(pygame.sprite.Sprite):
    def __init__(self, im, cut=False, *args):
        super().__init__(all_sprites)
        self.name = im
        self.price = 2
        self.vx = random.randrange(-2, 2)
        self.image = load_image(im)
        self.cut = cut
        self.flag = False
        if self.cut:
            self.rect = self.image.get_rect(center=(args[0][0], args[0][1]))
            if self.rect[0] <= 0:
                self.rect[0] = 0
        else:
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(10, 1001)
            self.top = random.randrange(20, 150)
            self.rect.y = 730

    def update(self, *args):
        global score
        draw_score(20, 20, score)
        draw_time(600, 20)
        if not self.cut:
            if self.rect.y <= self.top:
                self.flag = True
            if self.flag:
                self.rect = self.rect.move(self.vx, 5)
            else:
                self.rect = self.rect.move(self.vx, -5)
        else:
            self.rect = self.rect.move(self.vx, 8)

    def check(self, pos):
        global extra_time, score
        if int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                  self.rect.y +
                                                                                                  self.rect[
                                                                                                      3]) and self.name == 'Bomb.png':
            extra_time += 10
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                    self.rect.y +
                                                                                                    self.rect[
                                                                                                        3]) and self.name == 'Score_2x_Banana.png':
            score *= 2
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                    self.rect.y +
                                                                                                    self.rect[
                                                                                                        3]) and self.name == '5seconds_Banana.png':
            extra_time -= 5
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                    self.rect.y +
                                                                                                    self.rect[3]):
            return True
        else:
            return False

    def change(self):
        global score
        score += 1
        im = NAME_CHANGE[self.name]
        k = 0
        for el in im:
            Sprites(el, True, [self.rect[0] + 50 * k, self.rect[1], self.rect[2], self.rect[3]])
            k += 1
        all_sprites.remove(self)

    def sliced(self):
        return self.cut


def get_click(pos):
    for e in all_sprites:
        if not e.sliced():
            a = e.check(pos)
            if a:
                e.change()


class ClassicMode():
    def sprites_drawing(self):
        k = random.randrange(2, 5)
        global data
        data1 = data.copy()
        data1.remove('5seconds_Banana.png')
        data1.remove('Score_2x_Banana.png')
        for i in range(k):
            Sprites(data1[random.randrange(0, 11)])

    def update(self):
        pass


class ZenMode():
    def sprites_drawing(self):
        k = random.randrange(2, 5)
        global data
        data1 = data[:]
        data1.remove('5seconds_Banana.png')
        data1.remove('Score_2x_Banana.png')
        data1.remove('Bomb.png')
        for i in range(k):
            Sprites(data1[random.randrange(0, 7)])


class ArcadeMode():
    def sprites_drawing(self):
        k = random.randrange(2, 5)
        for i in range(k):
            global data
            Sprites(data[random.randrange(0, 7)])


scenes = {'Menu': Menu(),
          'Classic Mode': ClassicMode().sprites_drawing(), 'Zen Mode': ZenMode().sprites_drawing(), 'Arcade Mode':
              ArcadeMode().sprites_drawing()}
scene = scenes['Menu']


def terminate():
    pygame.quit()
    sys.exit()


def draw_score(x, y, score):  # рисует счет
    write_text(screen, str(score), 30, x, y)


def draw_time(x, y):
    write_text(screen, f'Осталось {str(60 - round(end_time - start_time + extra_time))} секунд', 30, x, y)


def game_over():  # завершение игры, вывод счета
    global cursor1, connect1, score
    cursor1.execute("""INSERT INTO result(res) VALUES(?)""", (str(score), ))
    connect1.commit()
    global run
    list_score = cursor1.execute("""SELECT res FROM result """).fetchall()
    r = max(list_score)
    game_over_text = [f'Вы набрали {score} очков',
                      f'Лучший результат {r[0]} ',
                      'Кликните чтобы продолжить']
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 546
    for line in game_over_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 550
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    score = 0
    global scene
    scene = scenes['Menu']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                if start_screen2():
                    return True
        pygame.display.flip()


def start_screen1():
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_screen2():
                    return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen2():
    global run
    intro_text = ["Правила игры", "",
                  "В игре существует несколько режимов: Zen, Classic, Arcade",
                  "Zen - нет бомб, жизни за пропущенный фрукт не отнимают,",
                  "  но у вас есть всего лишь 90 секунд, чтобы поставить рекорд.",
                  "Classic – у вас есть три жизни, которые отнимаются, если вы пропускаете фрукт.",
                  "  Касание бомб приводит к неизбежному game over.",
                  "Arcade – режим с ограниченным временем (одна минута),",
                  "  помимо обычных фруктов игра будет подбрасывать вам особые бананы,",
                  "  некоторые из них активируют режим slo-mo, ускоряют появление фруктов на экране или удваивают очки."
                  ]
    fon2 = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon2, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 10, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            scene.handle_event(event)
        if run:
            return True
        pygame.display.flip()
        clock.tick(FPS)


tile_images = load_image('background.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = tile_images
        self.rect = self.image.get_rect()

    def sliced(self):
        return True

    def check(self, pos):
        return False

    def change(self):
        pass


def generate_level():
    Tile()


pygame.init()
all_sprites = pygame.sprite.Group()
generate_level()
running = True
pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 1280, 730
screen = pygame.display.set_mode(size)
start_screen1()
start_time = time.time()
extra_time = 0


# Score_2x_Banana удваивает счет, 10seconds_Banana добавляет 10 секунд времени, Bomb отнимает 5 секунд


def job():
    k = random.randrange(2, 4)
    for i in range(k):
        Sprites(data[random.randrange(0, 13)])


schedule.every(2).seconds.do(job)

if __name__ == '__main__':
    while running:
        end_time = time.time()
        schedule.run_pending()  # запуск запланированных заданий
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                get_click(event.pos)
        for e in all_sprites:
            if e.rect.x < 0 or e.rect.x > WIDTH or e.rect.y < 0 or e.rect.y > HEIGHT:
                all_sprites.remove(e)
        if round(end_time - start_time + extra_time) >= 60:
            game_over()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

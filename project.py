import pygame
import random
import os

move_r = 0
move_l = 0
press_f = 0
point = 0
fire = 0
start = 0
timer = 0
life = 3
timer_timer = 0
col = 0
game_over = 0
launch = 0
lst_aliens = []
pygame.init()
width, height = 600, 800
size = width, height
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=-1):
    fulname = os.path.join("data", name)
    try:
        image = pygame.image.load(fulname)
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)


class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("black")
        self.font_color = pygame.Color("red")
        self.font = pygame.font.SysFont(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)


class Fon (pygame.sprite.Sprite):
    image = load_image("planet.png")
    def __init__(self, group):
        super().__init__(group)
        self.image = Fon.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Aliens (pygame.sprite.Sprite):
    image = load_image("Aliens.png")
    def __init__(self, group):
        super().__init__(group)
        self.image = Aliens.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 100)
        self.rect.y = -70

    def update(self):
        if (start == 1) and (game_over != 1):
            self.rect.y += 2

    def pos(self):
        return self.rect.y


class Heros (pygame.sprite.Sprite):
    image = load_image("Hero.png")
    X = 3

    def __init__(self, group):
        super().__init__(group)
        self.image = Heros.image
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 700
        self.dir_x = 0
        self.life = 3

    def update(self):
        if (start == 1) and (game_over != 1):
            if self.rect.x <= -100:
                self.rect.x = 700
            elif self.rect.x >= 700:
                self.rect.x = -100
            self.rect.x += Heros.X * self.dir_x
            if pygame.sprite.spritecollide(hero, aliens, True):
                self.life -= 1

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dir_x -= 1
            elif event.key == pygame.K_RIGHT:
                self.dir_x += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.dir_x += 1
            elif event.key == pygame.K_RIGHT:
                self.dir_x -= 1
    def condition(self):
        return [(self.life + (laser.condition()[1] // 5000)), self.rect.x]


class Lasers(pygame.sprite.Sprite):
    image = load_image("fire.png", -1)
    Y = 5
    X = 3

    def __init__(self, group):
        super().__init__(group)
        self.image = Lasers.image
        self.rect = self.image.get_rect()
        self.rect.x = 290
        self.rect.y = 800
        self.dir_x = 0
        self.y = 0
        self.x = 290
        self.point = 0
        self.p_point = 0

    def update(self):
        if self.y == 0:
            self.rect.x = hero.condition()[1] + 40
        if self.y == 1:
            self.rect.y  -= Lasers.Y
        if self.rect.y <= -70:
            self.rect.y = 800
            self.y = 0
            self.rect.x = hero.condition()[1] + 40
        if pygame.sprite.spritecollide(laser, aliens, True):
            self.rect.y = 800
            self.y = 0
            self.point += 100
            self.p_point += 100
            self.rect.x = hero.condition()[1] + 40
        for i in lst_aliens:
            if i.pos() == 790:
                if self.point >= 200:
                    self.point -= 200
                else:
                    self.point = 0
                lst_aliens.remove(i)


    def condition(self):
        return [self.point, self.p_point]



    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dir_x -= 1
            elif event.key == pygame.K_RIGHT:
                self.dir_x += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.dir_x += 1
            elif event.key == pygame.K_RIGHT:
                self.dir_x -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                if self.y == 0:
                    self.y = 1
                    self.rect.y = 700

p_e_gui = GUI()
game_over_gui = GUI()

p_e_gui.add_element(Label(((0, 300), (-100, 200)), " PRESS"))
p_e_gui.add_element(Label(((0, 400), (-100, 210)), " ENTER"))
game_over_gui.add_element(Label(((0, 300), (-100, 200)), " GAME"))
game_over_gui.add_element(Label(((0, 400), (-100, 210)), " OVER"))
label_l = Label(((0, 305), (0, 70)), " press left")
label_r = Label(((330, 300), (0, 70)), " press right")
label_f = Label(((0, 400), (0, 140)), " press spase")
aliens = pygame.sprite.Group()
lasers = pygame.sprite.Group()
heros = pygame.sprite.Group()
fon = pygame.sprite.Group()
Fon(fon)
laser = Lasers(lasers)
hero = Heros(heros)
alien = Aliens(aliens)
lst_aliens.append(alien)
v = 90
fps = 60
clock = pygame.time.Clock()
running = True
while running:
    label_point = Label(((0, 0), (0, 50)), str(laser.condition()[0]))
    label_life = Label(((580, 0), (0, 50)), str(hero.condition()[0]))
    fon.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                if start == 0:
                    start = 1
                    launch = 1
                else:
                    start = 0
            if event.key == 32:
                fire = 1
                press_f = 1
            if event.key == pygame.K_LEFT:
                move_l = 1
            if event.key == pygame.K_RIGHT:
                move_r = 1
        heros.sprites()[0].get_event(event)
        lasers.sprites()[0].get_event(event)

    if game_over != 1:
        if  (launch == 1):
            if (fire == 1):
               lasers.draw(screen)
            if start == 1:
               lasers.update()
        if (start == 1):
            if (move_l == 1) and (move_r == 1) and (press_f == 1):
                if (timer_timer == 400):
                    if (col != 200):
                        col += 20
                    timer_timer = 0
                if timer > 250 - col:
                    alien = Aliens(aliens)
                    lst_aliens.append(alien)
                    timer = 0
                timer += 1
                timer_timer += 1
                if hero.condition()[0] == 0:
                    game_over = 1
                aliens.update()
        aliens.draw(screen)
        heros.draw(screen)
        heros.update()
        if start == 0:
            p_e_gui.render(screen)
        else:
            if move_l == 0:
                label_l.render(screen)
            if move_r == 0:
                label_r.render(screen)
            if press_f == 0:
                label_f.render(screen)
    else:
        fon.draw(screen)
        game_over_gui.render(screen)

    label_point.render(screen)
    label_life.render(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

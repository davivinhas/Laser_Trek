import pygame
from random import randint, choice
from spaceship import Spaceship
from aliens import Aliens
from alien_laser import AlienLaser
import obstacle
from hellokitty import HelloKitty
from watermelon import Watermelon

pygame.init()
screen_x = 600
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y))


def menu_state():
    screen.fill('Black')
    menu1 = pygame.image.load('sprites/menu01.jpeg').convert()
    menu2 = pygame.image.load('sprites/menu02.jpg').convert()
    menus = [menu1, menu2]
    menu_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state()
        screen.blit(menus[int(menu_index)], (0, 0))
        menu_index += 0.002
        if menu_index >= len(menus):
            menu_index = 0
        pygame.display.update()


def game_state():
    screen.fill('Black')
    class Game:
        def __init__(self):
            global highscore
            # Nave
            spaceship_sprite = Spaceship((300, 550))
            self.spaceship = pygame.sprite.GroupSingle(spaceship_sprite)

            # Vida
            self.lifes = 3
            self.life_surface = pygame.image.load('sprites/HP.png').convert_alpha()
            self.life_surface = pygame.transform.scale(self.life_surface, (20, 20))
            self.life_position = screen_x - (self.life_surface.get_size()[0]) * 2 + 20

            # Pontuação
            self.score = 0
            self.font = pygame.font.Font(None, 30)

            # Aliens
            self.aliens = pygame.sprite.Group()
            self.alien_laser = pygame.sprite.Group()
            self.aliens_spawn(rows=5, cols=9, horizontal=60, vertical=50)

            # Obstáculos
            self.shape = obstacle.obstacle
            self.block_size = 6
            self.blocks = pygame.sprite.Group()
            self.obstacle_amount = 5
            self.obstacle_x_positions = [num * (screen_x / self.obstacle_amount) for num in range(self.obstacle_amount)]
            self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_x / 25, y_start=440)

            # power ups
            self.hellokitty = pygame.sprite.Group()
            self.watermelon = pygame.sprite.Group()

        def watermelon_spawn(self):
            watermelon_sprite = Watermelon((randint(0, 600), -20))
            self.watermelon.add(watermelon_sprite)

        def hellokitty_spawn(self):
            hellokitty_sprite = HelloKitty((randint(0, 600), -20))
            self.hellokitty.add(hellokitty_sprite)

        def create_obstacle(self, x_start, y_start, offset_x):
            for row_index, row in enumerate(self.shape):
                for col_index, col in enumerate(row):
                    if col == "x":
                        x = x_start + col_index * self.block_size + offset_x
                        y = y_start + row_index * self.block_size
                        block = obstacle.Block(self.block_size, 'Red', x, y)
                        self.blocks.add(block)

        def create_multiple_obstacles(self, *offset, x_start, y_start, ):
            for offset_x in offset:
                self.create_obstacle(x_start, y_start, offset_x)

        def aliens_spawn(self, rows, cols, horizontal, vertical):
            for row_index, row in enumerate(range(rows)):
                for col_index, col in enumerate(range(cols)):
                    x = col_index * horizontal + 45
                    y = row_index * vertical
                    alien_sprite = Aliens(choice(['slime', 'slime', 'slime', 'slime', 'squid', 'squid', 'eye']), x, y)
                    self.aliens.add(alien_sprite)

        def alien_shoot(self):  # Escolhe um alien aleatórto para atirar
            if self.aliens.sprites():
                random_alien = choice(self.aliens.sprites())
                alien_laser_sprite = AlienLaser(random_alien.rect.center)
                self.alien_laser.add(alien_laser_sprite)

        def collisions(self):
            if self.spaceship.sprite.laser:
                for laser in self.spaceship.sprite.laser:
                    alien_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                    if alien_hit:
                        for alien in alien_hit:
                            self.score += alien.value
                            laser.kill()
                    if pygame.sprite.spritecollide(laser, self.blocks, True):
                        laser.kill()

            if self.alien_laser:
                for laser in self.alien_laser:
                    if pygame.sprite.spritecollide(laser, self.blocks, True):
                        laser.kill()
                    if pygame.sprite.spritecollide(laser, self.spaceship, False):
                        laser.kill()
                        self.lifes -= 1
                        if self.lifes <= 0:
                            defeat_state()  # leva para a tela de derrota

            if self.aliens:  # leva para a tela de derrota
                for alien in self.aliens:
                    if alien.rect.bottom == 515:
                        defeat_state()
                    if pygame.sprite.spritecollide(alien, self.blocks, False):
                        defeat_state()

        def hellokitty_collision(self):
            if self.hellokitty:
                for kitty in self.hellokitty:
                    if pygame.sprite.spritecollide(kitty, self.spaceship, False):
                        kitty.kill()
                        if self.lifes < 3:
                            self.lifes += 1

        def watermelon_collision(self):
            if self.watermelon:
                for melon in self.watermelon:
                    if pygame.sprite.spritecollide(melon, self.spaceship, False):
                        melon.kill()
                        self.spaceship.sprite.laser_cooldown -= 200

        def display_lifes(self):
            for life in range(self.lifes):
                x = self.life_position + life * (self.life_surface.get_size()[0] - 45)
                screen.blit(self.life_surface, (x, 580))

        def display_score(self):
            score_surface = self.font.render(f'Score: {self.score}', False, 'white')
            score_rect = score_surface.get_rect(bottomleft=(0, 600))
            screen.blit(score_surface, score_rect)

        def victory(self):  # leva para a tela de vitória
            if len(self.aliens.sprites()) == 0:
                victory_state()

        def run(self):  # atualizar e desenhar os sprites
            self.spaceship.update()
            self.aliens.update()
            self.alien_laser.update()
            self.collisions()
            self.hellokitty.update()
            self.hellokitty_collision()
            self.watermelon.update()
            self.watermelon_collision()

            self.watermelon.draw(screen)
            self.hellokitty.draw(screen)
            self.aliens.draw(screen)
            self.alien_laser.draw(screen)
            self.spaceship.draw(screen)
            self.spaceship.sprite.laser.draw(screen)
            self.blocks.draw(screen)
            self.display_lifes()
            self.display_score()
            self.victory()

    # variáveis
    clock = pygame.time.Clock()
    FPS = 60
    game = Game()
    laser_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(laser_timer, 900)  # cooldown do tiro dos aliens
    kitty_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(kitty_timer, 30000)
    watermelon_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(watermelon_timer, 40000)

    # espaço
    space_surface = pygame.image.load('sprites/space2.0.jpg').convert()
    space_surface = pygame.transform.smoothscale(space_surface, (600, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == laser_timer:  # when the timer is triggered, a random alien shoots
                game.alien_shoot()
            if event.type == kitty_timer:
                game.hellokitty_spawn()
            if event.type == watermelon_timer:
                game.watermelon_spawn()

        screen.blit(space_surface, (0, 0))
        game.run()
        pygame.display.update()
        clock.tick(FPS)


def victory_state():
    screen.fill('Black')

    victory_surface = pygame.image.load('sprites/victory_screen.jpg').convert()
    victory_rect = victory_surface.get_rect(topleft=(0, 0))
    screen.blit(victory_surface, victory_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    menu_state()
        pygame.display.update()


def defeat_state():
    screen.fill('Black')
    defeat_surface = pygame.image.load('sprites/gameover_screen.jpg')
    defeat_surface = pygame.transform.scale(defeat_surface, (600, 600))
    defeat_rect = defeat_surface.get_rect(topleft=(0, 0))
    screen.blit(defeat_surface, defeat_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    menu_state()
        pygame.display.update()


menu_state()

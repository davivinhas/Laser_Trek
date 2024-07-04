import pygame
from laser import Laser


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.image.load('sprites/spaceship.png').convert_alpha()
        image = pygame.transform.scale(image, (32, 32))
        self.image = image
        self.rect = self.image.get_rect(midbottom=position)

        # Laser cooldown
        self.reloaded = True
        self.laser_timer = 0
        self.laser_cooldown = 800

        # Laser Sprite
        self.laser = pygame.sprite.Group()

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += 3
        elif keys[pygame.K_a]:
            self.rect.x -= 3
        if keys[pygame.K_SPACE] and self.reloaded:
            self.shoot()
            self.reloaded = False
            self.laser_timer = pygame.time.get_ticks()

    def limit(self):
        if self.rect.right >= 600:
            self.rect.right = 600
        if self.rect.left <= 0:
            self.rect.left = 0

    def shoot(self):
        self.laser.add(Laser(self.rect.center))

    def reloading(self):
        if not self.reloaded:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_timer >= self.laser_cooldown:
                self.reloaded = True

    def update(self):
        self.controls()
        self.limit()
        self.reloading()
        self.laser.update()

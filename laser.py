import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('sprites/laser.png')
        self.rect = self.image.get_rect(center=position)

    def movement(self):
        self.rect.y -= 5

    def destroy(self):
        if self.rect.y <= -20:
            self.kill()

    def update(self):
        self.movement()
        self.destroy()

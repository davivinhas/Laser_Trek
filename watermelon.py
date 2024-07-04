import pygame


class Watermelon(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load('sprites/watermelon.png')
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect(center=position)

    def movement(self):
        self.rect.y += 4

    def destroy(self):
        if self.rect.y >= 650:
            self.kill()

    def update(self):
        self.movement()
        self.destroy()
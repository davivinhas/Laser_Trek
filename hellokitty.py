import pygame


class HelloKitty(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image1 = pygame.image.load('sprites/hellokitty1.png')
        image1 = pygame.transform.scale(image1, (25, 25))
        image2 = pygame.image.load('sprites/hellokitty2.png')
        image2 = pygame.transform.scale(image2, (25, 25))
        self.images = [image1, image2]
        self.image_index = 0
        self.position = position
        self.image = self.images[int(self.image_index)]
        self.rect = self.image.get_rect(center=self.position)

    def movement(self):
        self.rect.y += 4

    def animation(self):
        self.image_index += 0.03
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def destroy(self):
        if self.rect.y >= 650:
            self.kill()

    def update(self):
        self.animation()
        self.destroy()
        self.movement()

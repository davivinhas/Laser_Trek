import pygame


class Aliens(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()

        match type:
            case 'squid':
                image1 = pygame.image.load('sprites/Lula1.png').convert_alpha()
                image2 = pygame.image.load('sprites/Lula2.png').convert_alpha()
                image3 = pygame.image.load('sprites/Lula3.png').convert_alpha()
                image4 = pygame.image.load('sprites/Lula4.png').convert_alpha()
                image1 = pygame.transform.scale(image1, (32, 32))
                image2 = pygame.transform.scale(image2, (32, 32))
                image3 = pygame.transform.scale(image3, (32, 32))
                image4 = pygame.transform.scale(image4, (32, 32))
                self.images = [image1, image2, image3, image4]
                self.value = 200

            case 'eye':
                image1 = pygame.image.load('sprites/eye1.png').convert_alpha()
                image2 = pygame.image.load('sprites/eye2.png').convert_alpha()
                image3 = pygame.image.load('sprites/eye1.png').convert_alpha()
                image4 = pygame.image.load('sprites/eye3.png').convert_alpha()
                image1 = pygame.transform.scale(image1, (32, 32))
                image2 = pygame.transform.scale(image2, (32, 32))
                image3 = pygame.transform.scale(image3, (32, 32))
                image4 = pygame.transform.scale(image4, (32, 32))
                self.images = [image1, image2, image3, image4]
                self.value = 300
            case 'slime':
                image1 = pygame.image.load('sprites/slime1.png').convert_alpha()
                image2 = pygame.image.load('sprites/slime2.png').convert_alpha()
                image1 = pygame.transform.scale(image1, (32, 32))
                image2 = pygame.transform.scale(image2, (32, 32))
                self.images = [image1, image2]
                self.value = 100

        self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.move_counter = 0
        self.move = 1

    def animation(self):
        self.animation_index += 0.04
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
    def movement(self):
        self.rect.x += self.move
        self.move_counter += 1
        if abs(self.move_counter) >= 30:
            self.move *= -1
            self.rect.y += 1.45
            self.move_counter *= self.move

    def update(self):
        self.animation()
        self.movement()

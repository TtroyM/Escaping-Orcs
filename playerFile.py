import pygame
import os

class Player:
    NAME_FILE = 'player_name.txt'

    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = self.load_player_name()

    def move(self, keys, width, height):
        if keys[pygame.K_a] and self.x - self.vel >= 0:
            self.x -= self.vel
        if keys[pygame.K_d] and self.x + self.vel + self.width <= width:
            self.x += self.vel
        if keys[pygame.K_w] and self.y - self.vel >= 0:
            self.y -= self.vel
        if keys[pygame.K_s] and self.y + self.vel + self.height <= height:
            self.y += self.vel
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (self.x,self.y) #rect updated w position

    def scale(self, scale_factor):
        self.width = int(self.width * scale_factor)
        self.height = int(self.height * scale_factor)
        self.x = int(self.x * scale_factor)
        self.y = int(self.y * scale_factor)
        self.update_rect()

    def draw(self, win, image):
        win.blit(image, (self.x, self.y))

    def load_player_name(self):
        if os.path.exists(self.NAME_FILE):
            with open(self.NAME_FILE, 'r') as f:
                return f.read().strip()
        return None

    def save_player_name(self):
        if self.name:
            with open(self.NAME_FILE, 'w') as f:
                f.write(self.name)

    def get_player_name(self, win, font):
        if self.name:
            return self.name
        
        name = ""
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            
            win.fill((0, 0, 0))
            prompt_text = font.render("Enter your name: " + name, 1, (255, 255, 255))
            win.blit(prompt_text, (win.get_width() // 2 - prompt_text.get_width() // 2, win.get_height() // 2))
            pygame.display.update()

        self.name = name
        self.save_player_name()
        return name

    

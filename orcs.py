import pygame
pygame.font.init()

class Orc:
  def __init__(self,x,y, color=(0,255,0), hp=3, image=None, stronger_orc=False):
    self.x = x
    self.y = y
    self.width = 70
    self.height = 90
    self.vel = 1
    self.color = color
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hp = hp
    self.stronger_orc = stronger_orc
    self.image = image

    if self.image:
      self.image = pygame.transform.scale(self.image, (self.width, self.height))

  def move_towards_player(self, player):
    if self.x < player.x:
      self.x += self.vel
    elif self.x > player.x:
      self.x -= self.vel
    if self.y < player.y:
      self.y += self.vel
    elif self.y > player.y:
      self.y -= self.vel
    self.update_hitbox()

  def update_hitbox(self):
    self.hitbox.update(self.x,self.y,self.width,self.height)

  def draw(self, win):
    if self.image:
      win.blit(self.image, (self.x, self.y))
    else:
      pygame.draw.rect(win, self.color, self.hitbox)

  def scale(self, scale_factor):
    self.width = int(70 * scale_factor)
    self.height = int(90 * scale_factor)
    self.x = int(self.x * scale_factor)
    self.y = int(self.y * scale_factor)
    if self.image:
      self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.update_hitbox()
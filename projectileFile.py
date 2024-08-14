import pygame
import math

class Projectile:
  def __init__(self, x, y, target_x, target_y):
    self.x = x
    self.y = y
    self.radius = 5
    self.color = (0,255,255)
    self.vel = 8

    angle = math.atan2(target_y - y, target_x - x)
    self.dx = self.vel * math.cos(angle)
    self.dy = self.vel * math.sin(angle)
    self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

  def move(self):
    self.x += self.dx
    self.y += self.dy
    self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
    
  def draw(self,win):
    pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
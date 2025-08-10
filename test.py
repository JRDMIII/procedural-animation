import pygame
import math

pos_1 = pygame.Vector2(1, 1)

new_vec = pygame.Vector2(
    pos_1.x * math.cos(120) - pos_1.y * math.sin(120),
    pos_1.x * math.sin(120) + pos_1.y * math.cos(120)
)

print(new_vec)
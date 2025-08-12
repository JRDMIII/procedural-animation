import pygame
from Ant import Ant
import math
import random

def main():
    # Setting up pygame environment
    pygame.init()

    SCREEN_WIDTH = 1800
    SCREEN_HEIGHT = 1000
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial", 12)

    # Setting up the display
    pygame.display.set_caption("Procedural Animation")
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    ant = Ant((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Bool to control the main loop
    running = True

    current_angle = 0    

    GRANITE = (25, 25, 25)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        a = 350  # size of the infinity sign
        current_angle = (current_angle + 0.005) % (2 * math.pi)

        # Lemniscate of Gerono
        ant.set_target_position(pygame.Vector2(center.x + a * math.cos(current_angle), center.y + a * math.sin(current_angle) * math.cos(current_angle)))

        # mouse_pos = pygame.mouse.get_pos()
        # ant.set_target_position(mouse_pos)
            
        SCREEN.fill(GRANITE)

        # fps = CLOCK.get_fps()
        # fps_text = FONT.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        # SCREEN.blit(fps_text, (10, 10))
        
        ant.step()
        ant.draw(SCREEN)
        
        pygame.display.flip()

        # Cap frame rate
        CLOCK.tick(200)
    
if __name__ == "__main__":
    # cProfile.run('main()', sort='cumtime')
    main()
import pygame
from Skeleton import Skeleton

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

    skeleton = Skeleton(10, 50, (SCREEN_WIDTH, SCREEN_HEIGHT), 110)
    print(skeleton)

    # Bool to control the main loop
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        SCREEN.fill((15, 15, 15))
        
        skeleton.step()
        skeleton.draw(SCREEN)
        
        pygame.display.flip()

        # Cap frame rate
        CLOCK.tick(165)
    
main()
import pygame
from Leg import Leg

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

    leg = Leg(4, (SCREEN_WIDTH, SCREEN_HEIGHT), 70)
    print(leg)

    # Bool to control the main loop
    running = True

    while running:
        avg = (0, 0)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        leg.set_target_point(mouse_pos)
            
        SCREEN.fill((15, 15, 15))

        # fps = CLOCK.get_fps()
        # fps_text = FONT.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        # SCREEN.blit(fps_text, (10, 10))
        
        leg.step()
        leg.draw(SCREEN)
        
        pygame.display.flip()

        # Cap frame rate
        CLOCK.tick(60)
    
main()
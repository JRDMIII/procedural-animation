from Dot import Dot
import pygame
import math

class Skeleton:
    # Defining parameters
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around
    dot_dist: int
    dimensions: pygame.Vector2

    def __init__(self, length, dist, dimensions):
        self.length = length    
        self.anchor = None      
        self.dot_dist = dist
        self.dimensions = pygame.Vector2(
            dimensions[0],
            dimensions[1]
        )

        # Debug
        self.current_angle = 0
        self.angle_step = 0.1

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0, self.dot_dist, pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2))
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_child(Dot(id, self.dot_dist, pygame.Vector2(0, 0)))
            current_dot = current_dot.child
        
        current_dot.child = None
        
    def step(self):
        # velocity = pygame.Vector2(math.cos(self.current_angle)*3, math.sin(self.current_angle)*3)
        # self.current_angle = (self.current_angle + 5) % 360

        # self.anchor.position += velocity
    
        center = pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2)
        radius = 200
        self.current_angle = (self.current_angle + 0.05) % (2 * math.pi)

        # Update anchor position
        self.anchor.position.x = center.x + radius * math.cos(self.current_angle)
        self.anchor.position.y = center.y + radius * math.sin(self.current_angle)

        # Loop through all dots and constrain them
        current_dot = self.anchor
        
        while current_dot != None:
            current_dot.constrain_child()
            current_dot = current_dot.child
        
    def draw(self, screen):
        current_dot = self.anchor

        while current_dot != None:
            pygame.draw.circle(screen, (255, 255, 255), current_dot.position, 10, 3)
            current_dot = current_dot.child

    
if __name__ == "__main__":
    skeleton = Skeleton(3, 50)
    current_dot = skeleton.anchor

    while current_dot != None:
        print(current_dot.position)
        current_dot = current_dot.child
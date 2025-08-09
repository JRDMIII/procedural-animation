from Dot import Dot
import pygame

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

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0, self.dot_dist, pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2))
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_child(Dot(id, self.dot_dist, pygame.Vector2(0, 0)))
            current_dot.constrain_child()
            current_dot = current_dot.child
        
    def draw(self, screen):
        current_dot = self.anchor

        while current_dot != None:
            pygame.draw.circle(screen, (255, 255, 255), current_dot.position, 5, 3)
            current_dot = current_dot.child

    
if __name__ == "__main__":
    skeleton = Skeleton(3, 50)
    current_dot = skeleton.anchor

    while current_dot != None:
        print(current_dot.position)
        current_dot = current_dot.child
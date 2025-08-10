from Dot import Dot
import pygame
import math

class Skeleton:
    # Defining parameters
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around
    dot_dist: int
    dimensions: pygame.Vector2

    def __init__(self, length, dist, dimensions, angle_thresh):
        self.length = length    
        self.anchor = None      
        self.dot_dist = dist
        self.angle_thresh = angle_thresh

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
        previous_dot = None
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_parent(previous_dot)
            current_dot.add_child(Dot(id, self.dot_dist, pygame.Vector2(0, 0)))

            previous_dot = current_dot
            current_dot = current_dot.child
        
        current_dot.child = None
        current_dot.parent = previous_dot
        
    def step(self):
        # velocity = pygame.Vector2(math.cos(self.current_angle)*3, math.sin(self.current_angle)*3)
        # self.current_angle = (self.current_angle + 5) % 360

        # self.anchor.position += velocity
    
        center = pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2)
        a = 300  # size of the infinity sign
        self.current_angle = (self.current_angle + 0.02) % (2 * math.pi)

        # Lemniscate of Gerono
        self.anchor.position.x = center.x + a * math.cos(self.current_angle)
        self.anchor.position.y = center.y + a * math.sin(self.current_angle) * math.cos(self.current_angle)

        # Loop through all dots and constrain them
        current_dot:Dot = self.anchor
        
        while current_dot != None:
            current_dot.constrain_child(self.angle_thresh)
            current_dot = current_dot.child
        
    def draw(self, screen):
        current_dot = self.anchor

        while current_dot != None:
            pygame.draw.circle(screen,
                (255, 0, 0) if current_dot.id == 0  else (255, 255, 255), 
                current_dot.position, 10, 3)
            current_dot = current_dot.child
        
    def __str__(self):
        string = ""

        current_dot = self.anchor
        
        while current_dot != None:
            string += current_dot.__str__() + "\n"
            current_dot = current_dot.child
        
        return string

    
if __name__ == "__main__":
    skeleton = Skeleton(3, 50, (500, 500))
    print(skeleton)
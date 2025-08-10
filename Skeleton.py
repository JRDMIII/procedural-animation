from Dot import Dot
import pygame
import math

class Skeleton:
    # Defining parameters
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around
    dot_distances: list[int]
    dimensions: pygame.Vector2
    dot_sizes: list[int]

    def __init__(self, length, dimensions, angle_thresh, dot_sizes:list[int], dot_distances:list[int]):
        self.length = length    
        self.anchor = None      
        self.dot_distances = dot_distances
        self.angle_thresh = angle_thresh
        self.dot_sizes = dot_sizes

        # Checking to see if we have the same amount of sizes and dots
        if not len(dot_sizes) == self.length:
            while len(dot_sizes) != self.length:
                dot_sizes.append(5)

        self.dimensions = pygame.Vector2(
            dimensions[0],
            dimensions[1]
        )

        self.current_angle = 0

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0, self.dot_distances[0], pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2))
        previous_dot = None
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_parent(previous_dot)
            current_dot.add_child(Dot(id, self.dot_distances[id], pygame.Vector2(0, 0)))

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
                current_dot.position, self.dot_sizes[current_dot.id], 3)
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
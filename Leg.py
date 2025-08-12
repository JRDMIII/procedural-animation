from Dot import Dot
import pygame

class Leg:
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around
    dimensions: pygame.Vector2
    anchor_point: pygame.Vector2
    angle_thresh: int
    segment_length: int

    def __init__(self, length, dimensions, angle_thresh, segment_length):
        self.dimensions = pygame.Vector2(
            dimensions[0],
            dimensions[1]
        )
        
        self.segment_length = segment_length
        self.anchor_point = pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2)
        self.target_point = pygame.Vector2(0, 0)
        self.current_target_point = self.target_point
        self.target_point_moving = False
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 2
        self.steps_moving = 0

        self.length = length
        self.angle_thresh = angle_thresh

        self.iterations = 50

        self.anchor = None
        self.endpoint = None

        self.setup_leg()
    
    def set_target_point(self, point: pygame.Vector2):
        """Change the target point of the leg"""
        self.target_point = point
        self.on_target_point_changed()

    def on_target_point_changed(self):
        """Event function for when the target point is changed"""
        self.target_point_moving = True
        
    def move_target_point(self):
        """Move the current target point linearly towards the new target position"""
        # Get direction to next point
        if self.target_point.distance_to(self.current_target_point) < 5 or self.steps_moving == 10:
            self.target_point_moving = False
            self.steps_moving = 0
            self.current_target_point = self.target_point

            self.velocity.x, self.velocity.y = 0, 0
            return

        dir = (self.target_point - self.current_target_point).normalize()
        self.velocity.xy += (self.acceleration * dir.x, self.acceleration * dir.y)
        self.current_target_point += self.velocity

    def setup_leg(self):
        """Sets up all dots in the leg"""
        self.anchor = Dot(0, self.segment_length, pygame.Vector2(self.dimensions.x / 2, self.dimensions.y / 2))
        previous_dot = None
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_parent(previous_dot)
            current_dot.add_child(Dot(id, self.segment_length, pygame.Vector2(0, 0)))

            previous_dot = current_dot
            current_dot = current_dot.child
        
        current_dot.child = None
        current_dot.parent = previous_dot
        self.endpoint = current_dot
    
        # Loop through all dots and constrain them
        current_dot:Dot = self.anchor
        
        while current_dot != None:
            current_dot.constrain_child(self.angle_thresh)
            current_dot = current_dot.child
    
    def draw(self, screen):
        current_dot = self.anchor

        while current_dot != None:
            # pygame.draw.circle(screen,
            #     (255, 0, 0) if current_dot.id == 0  else (255, 255, 255), 
            #     current_dot.position, 4, 3)
            
            pygame.draw.circle(screen,
                (240, 220, 180) if current_dot.id == 0  else (240, 220, 180), 
                current_dot.position, 4, 3)
            
            # Draw a line to the child if it exists
            if current_dot.child is not None:
                pygame.draw.line(
                    screen,
                    (240, 220, 180),  # Line color
                    current_dot.position,
                    current_dot.child.position,
                    4  # Line thickness
                )

            current_dot = current_dot.child
        
        # pygame.draw.circle(screen, (255, 0, 0), self.target_point, 2, 2)

    def step(self):
        """Steps the leg forward"""
        # If we are moving the target point, move it
        if self.target_point_moving:
            self.steps_moving += 1
            self.move_target_point()

        # Perform fabrik calculation
        self.fabrik()

    
    def fabrik(self):
        """Performs the fabrik algorithm"""
        for _ in range(0, self.iterations):
            # Forward
            self.endpoint.position = self.current_target_point
            current_dot = self.endpoint
            while current_dot != None:
                current_dot.constrain_parent(self.angle_thresh)
                current_dot = current_dot.parent
            
            # Backward
            self.anchor.position = self.anchor_point
            current_dot = self.anchor
            while current_dot != None:
                current_dot.constrain_child(self.angle_thresh)
                current_dot = current_dot.child
            
    def __str__(self):
        string = ""

        current_dot = self.anchor
        
        while current_dot != None:
            string += current_dot.__str__() + "\n"
            current_dot = current_dot.child
        
        string += f"endpoint: {self.endpoint} \n"
        
        return string
            
if __name__ == "__main__":
    leg = Leg(3, (500, 500), 120)
    print(leg)
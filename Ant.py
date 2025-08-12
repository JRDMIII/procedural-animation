import pygame
from Dot import Dot
from Skeleton import Skeleton
from Leg import Leg
import math
from types import SimpleNamespace

class Ant:
    skeleton: Skeleton

    left_front: Leg
    left_middle: Leg
    left_back: Leg

    right_front: Leg
    right_middle: Leg
    right_back: Leg

    velocity: pygame.Vector2
    max_velocity: int
    acceleration: int
    target_position: pygame.Vector2
    moving: bool

    def __init__(self, dimensions):
        self.dimensions = pygame.Vector2(
            dimensions[0],
            dimensions[1]
        )

        self.skeleton = Skeleton(3, (self.dimensions.x, self.dimensions.y), 110, [15, 10, 20], [25, 30, 0])
        
        self.left_front = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 25)
        self.left_middle = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 28)
        self.left_back = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 25)

        self.right_front = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 25)
        self.right_middle = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 28)
        self.right_back = Leg(3, (self.dimensions.x, self.dimensions.y), 20, 25)

        self.skeleton.step()

        self.target_position = pygame.Vector2(self.dimensions.x, self.dimensions.y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 2
        self.max_velocity = 3
        self.moving = False

        self.front_params = {
            "anchor_vert": -5,
            "horizontal": 40,
            "vertical": -80,
            "dist": 80
        }

        self.middle_params = {
            "anchor_vert": 0,
            "horizontal": 45,
            "vertical": -40,
            "dist": 70
        }

        self.back_params = {
            "anchor_vert": 15,
            "horizontal": 35,
            "vertical": -20,
            "dist": 70
        }

        self.legs = [
            self.left_front,
            self.right_front,
            self.left_middle,
            self.right_middle,
            self.left_back,
            self.right_back,
        ]
    
    def set_target_position(self, position: pygame.Vector2):
        self.target_position.xy = (position[0], position[1])
        self.moving = True

    def step_legs(self, left:Leg, right:Leg, params):
        """Sets the back legs target position and moves the back legs"""

        # Step the middle left and right legs

        point_1 = self.skeleton.anchor.child.position
        point_2 = self.skeleton.anchor.child.child.position

        # Get vector for those two
        dir_vector = (point_2 - point_1).normalize()

        right.anchor_point = self.skeleton.anchor.child.position + (dir_vector * params["anchor_vert"])
        left.anchor_point = self.skeleton.anchor.child.position  + (dir_vector * params["anchor_vert"])
        
        angle = math.radians(-90)
        a_cos, a_sin = math.cos(angle), math.sin(angle)

        # Rotate the parent vector by the exact amount for the parent threshold
        new_vec = pygame.Vector2(
            dir_vector.x * a_cos - dir_vector.y * a_sin,
            dir_vector.x * a_sin + dir_vector.y * a_cos
        ) * params["horizontal"]

        left_target_point = left.anchor_point + new_vec + (dir_vector * params["vertical"])
        right_target_point = right.anchor_point + (new_vec * -1) + (dir_vector * params["vertical"])

        if left.target_point.distance_to(left_target_point) > params["dist"]:
            left.set_target_point(left_target_point)
        
        if right.target_point.distance_to(right_target_point) > params["dist"]:
            right.set_target_point(right_target_point)

        left.step()
        right.step()

    def step(self):
        if self.moving:
            if abs(self.target_position.distance_to(self.skeleton.anchor.position)) < 50:
                self.moving = False
            else:
                dir = (self.target_position - self.skeleton.anchor.position).normalize()

                self.velocity += dir * self.acceleration

                if self.velocity.magnitude() > self.max_velocity:
                    self.velocity = self.velocity.normalize() * self.max_velocity
                
                self.skeleton.anchor.position += self.velocity

        self.skeleton.step()

        self.step_legs(self.left_front, self.right_front, self.front_params)
        self.step_legs(self.left_middle, self.right_middle, self.middle_params)
        self.step_legs(self.left_back, self.right_back, self.back_params)
        
    def draw(self, screen):
        for leg in self.legs:
            leg.draw(screen)

        self.skeleton.draw(screen)

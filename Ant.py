import pygame
from Dot import Dot
from Skeleton import Skeleton
from Leg import Leg
import math

class Ant:
    skeleton: Skeleton

    left_front: Leg
    left_middle: Leg
    left_back: Leg

    right_front: Leg
    right_middle: Leg
    right_back: Leg

    leg_anchor_points: list[pygame.Vector2]

    def __init__(self, dimensions):
        self.dimensions = pygame.Vector2(
            dimensions[0],
            dimensions[1]
        )

        self.skeleton = Skeleton(3, (self.dimensions.x, self.dimensions.y), 110, [20, 10, 30], [30, 40, 0])
        
        self.left_front = Leg(3, (self.dimensions.x, self.dimensions.y), 20)
        self.left_middle = Leg(3, (self.dimensions.x, self.dimensions.y), 20)
        self.left_back = Leg(3, (self.dimensions.x, self.dimensions.y), 20)

        self.right_front = Leg(3, (self.dimensions.x, self.dimensions.y), 20)
        self.right_middle = Leg(3, (self.dimensions.x, self.dimensions.y), 20)
        self.right_back = Leg(3, (self.dimensions.x, self.dimensions.y), 20)

        self.skeleton.step()

        self.leg_anchor_points = [
            self.skeleton.anchor.position,
            self.skeleton.anchor.child.position,
        ]

        self.setup_ant()

    def setup_ant(self):
        """Sets up all elements of the ant"""
        self.right_front.anchor_point = self.leg_anchor_points[0]
        self.left_front.anchor_point = self.leg_anchor_points[0]

        self.right_middle.anchor_point = self.leg_anchor_points[1]
        self.left_middle.anchor_point = self.leg_anchor_points[1]

        self.right_back.anchor_point = self.leg_anchor_points[1]
        self.left_back.anchor_point = self.leg_anchor_points[1]
    
    def step_front_legs(self):
        """Sets the front legs target position and moves the front legs"""

        # Step the front left and right legs

        point_1 = self.skeleton.anchor.position
        point_2 = self.skeleton.anchor.child.position

        # Get vector for those two
        dir_vector = (point_2 - point_1).normalize()
        
        # Rotate the parent vector by the exact amount for the parent threshold
        new_vec = pygame.Vector2(
            dir_vector.x * math.cos(math.radians(-90)) - dir_vector.y * math.sin(math.radians(-90)),
            dir_vector.x * math.sin(math.radians(-90)) + dir_vector.y * math.cos(math.radians(-90))
        ) * 50

        new_left_vec = new_vec - (dir_vector * 50)
        new_right_vec = (new_vec * -1) - (dir_vector * 50)

        left_target_point = self.leg_anchor_points[0] + new_left_vec
        right_target_point = self.leg_anchor_points[0] + new_right_vec

        if self.left_front.target_point.distance_to(left_target_point) > 80:
            self.left_front.set_target_point(left_target_point)
        
        if self.right_front.target_point.distance_to(right_target_point) > 80:
            self.right_front.set_target_point(right_target_point)

        self.left_front.step()
        self.right_front.step()

    def step_mid_legs(self):
        """Sets the mid legs target position and moves the mid legs"""
        # Step the middle left and right legs
        
        self.right_middle.anchor_point = self.skeleton.anchor.child.position
        self.left_middle.anchor_point = self.skeleton.anchor.child.position

        point_1 = self.skeleton.anchor.child.position
        point_2 = self.skeleton.anchor.child.child.position

        # Get vector for those two
        dir_vector = (point_2 - point_1).normalize()
        
        # Rotate the parent vector by the exact amount for the parent threshold
        new_vec = pygame.Vector2(
            dir_vector.x * math.cos(math.radians(-90)) - dir_vector.y * math.sin(math.radians(-90)),
            dir_vector.x * math.sin(math.radians(-90)) + dir_vector.y * math.cos(math.radians(-90))
        ) * 50

        new_left_vec = new_vec - (dir_vector * 50)
        new_right_vec = (new_vec * -1) - (dir_vector * 50)

        left_target_point = self.left_middle.anchor_point + new_left_vec
        right_target_point = self.right_middle.anchor_point + new_right_vec

        if self.left_middle.target_point.distance_to(left_target_point) > 70:
            self.left_middle.set_target_point(left_target_point)
        
        if self.right_middle.target_point.distance_to(right_target_point) > 70:
            self.right_middle.set_target_point(right_target_point)

        self.left_middle.step()
        self.right_middle.step()

    def step_back_legs(self):
        """Sets the back legs target position and moves the back legs"""

        # Step the middle left and right legs

        point_1 = self.skeleton.anchor.child.position
        point_2 = self.skeleton.anchor.child.child.position

        # Get vector for those two
        dir_vector = (point_2 - point_1).normalize()

        self.right_back.anchor_point = self.skeleton.anchor.child.position + (dir_vector * 15)
        self.left_back.anchor_point = self.skeleton.anchor.child.position  + (dir_vector * 15)
        
        # Rotate the parent vector by the exact amount for the parent threshold
        new_vec = pygame.Vector2(
            dir_vector.x * math.cos(math.radians(-90)) - dir_vector.y * math.sin(math.radians(-90)),
            dir_vector.x * math.sin(math.radians(-90)) + dir_vector.y * math.cos(math.radians(-90))
        ) * 50

        new_left_vec = new_vec - (dir_vector * 50)
        new_right_vec = (new_vec * -1) - (dir_vector * 50)

        left_target_point = self.left_back.anchor_point + new_left_vec
        right_target_point = self.right_back.anchor_point + new_right_vec

        if self.left_back.target_point.distance_to(left_target_point) > 70:
            self.left_back.set_target_point(left_target_point)
        
        if self.right_back.target_point.distance_to(right_target_point) > 70:
            self.right_back.set_target_point(right_target_point)

        self.left_back.step()
        self.right_back.step()

    def step(self):
        self.skeleton.step()

        self.step_front_legs()
        self.step_mid_legs()
        self.step_back_legs()
        
    def draw(self, screen):
        self.left_front.draw(screen)
        self.right_front.draw(screen)
        
        self.left_middle.draw(screen)
        self.right_middle.draw(screen)

        self.left_back.draw(screen)
        self.right_back.draw(screen)

        self.skeleton.draw(screen)

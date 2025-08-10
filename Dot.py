import pygame
import math

class Dot:
    id: int # Position in the dot list
    child: 'Dot | None' # Child dot of this object
    parent: 'Dot | None' # Child dot of this object
    dist: int # Distance to constrain child to
    position: pygame.Vector2 # Current position of the dot

    def __init__(self, id, dist=None, pos=None):
        self.id = id
        self.child = None
        self.parent = None
        self.dist = dist
        self.position = pos
    
    def add_child(self, child):
        """Assign a child to this dot object"""
        self.child = child
    
    def add_parent(self, parent):
        """Assign a parent to this dot object"""
        self.parent = parent

    def constrain_child(self, angle_thresh):
        """Constrain the child to be in the radius defined in the skeleton"""

        # Check if the dot has a child
        if self.child != None:
            # Calculate vector going from parent to child
            direction_vector = self.child.position - self.position

            # Get normalised direction vector and multiply it by distance between points
            direction_vector = direction_vector.normalize() * self.dist

            # Move child to current position + direction vector
            self.child.position = self.position + direction_vector

        # Check if we have a grandparent (i guess?)
        if self.parent != None and self.parent.parent != None:
            parent = self.parent.parent
            middle = self.parent

            # Calculate the 2 vectors
            parent_vec:pygame.Vector2 = parent.position - middle.position
            child_vec:pygame.Vector2 = self.position - middle.position

            # Calculate the angle between the two vectors
            angle = parent_vec.angle_to(child_vec)

            # If we are out of the angle threshold
            if abs(angle) < angle_thresh or abs(angle) > (360 - angle_thresh):

                norm_vec = parent_vec.normalize()

                set_angle = angle_thresh if angle < angle_thresh else (360 - angle_thresh)

                # Rotate the parent vector by the exact amount for the parent threshold
                new_vec = pygame.Vector2(
                    norm_vec.x * math.cos(math.radians(set_angle)) - norm_vec.y * math.sin(math.radians(set_angle)),
                    norm_vec.x * math.sin(math.radians(set_angle)) + norm_vec.y * math.cos(math.radians(set_angle))
                ) * self.dist

                # Set our position to be our parents position + the vector to get to the correct angle
                self.position = middle.position + new_vec

    def move(self, velocity):
        self.position += velocity
    
    def __str__(self):
        return f"""
        id: {self.id}
        parent: {None if self.parent == None else self.parent.id}
        child: {None if self.child == None else self.child.id}
        """
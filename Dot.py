import pygame

class Dot:
    id: int             # Position in the dot list
    child: 'Dot | None' # Child dot of this object
    dist: int           # Distance to constrain child to
    position: pygame.Vector2 # Current position of the dot

    def __init__(self, id, dist=None, pos=None):
        self.id = id 
        self.child = None
        self.dist = dist
        self.position = pos
    
    def add_child(self, child):
        """Assign a child to this dot object"""
        self.child = child
    
    def constrain_child(self):
        """Constrain the child to be in the radius defined in the skeleton"""

        # Check if the dot has a child
        if self.child == None:
            return

        # Calculate vector going from parent to child
        direction_vector = self.child.position - self.position

        # Get normalised direction vector and multiply it by distance between points
        direction_vector = direction_vector.normalize() * self.dist

        # Move child to current position + direction vector
        self.child.position = self.position + direction_vector
    
    def move(self, velocity):
        self.position += velocity
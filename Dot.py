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
        self.child.position = self.position + pygame.Vector2(self.dist, 0)
# Dev Log: Procedural Animation

## The Theory
After looking it at too much rainworld content I have become very obsessed with the idea of procedural animation and specifically locomotion that isn't predefined with sprites. Hence, I will be exploring the ideas of procedural animation, hopefully making some cool things along the way!

I want to start with making a snake/worm like creature using the basic ideas of procedural animation and chained contraints. From there I want to try and make legs which move realistically and then finally make an ant which can move aroundthe environment, turning and walking and living life.

## Log 1: Understanding Procedural Animation

The lovely argonaut created a video discussing the basic technique of procedural animation[^1] - specifically starting with chained contraints which seem to be able to do most of what I need to for the first snake. I essentially needed to make a linked-list-style structure where each point on the object is connected to the one infront of it as a parent with a certain distance contraint. There should also be a main anchor which does all the movement and all the other points follow through the constraints.

I started by creating a basic world that the procedurally animated snake will run in using a default pygame environment from previous projects. Next, it was time to create the data structure that will hold the information for the procedurally animated line (for speed, it will be called a skeleton).

```python
class Dot:
    def __init__(self, id):
        self.id = 1 # Position in the dot list
        self.child = None
    
    def add_child(self, child):
        """Assign a child to this dot object"""
        self.child = child
```

I am of course still figuring out what will need to be done for this but at this very moment I think this should be enough to just create the structure. From there, I then setup a class which will hold all the dots in a skeleton so that mass updates can be performed:

```python
from Dot import Dot

class Skeleton:
    def __init__(self, length):
        self.length = length    # Length of the skeleton
        self.anchor = None      # The dot that is moved around

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0)
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_child(Dot(id))
        
        print(self.anchor.child != None)
```

Once again, this will be updated as I find out what does and doesn't work.

An interesting thing I immediately noticed was how similar it was to linked lists, especially the setup of the skeleton where we loop through, adding a child to dots then making the current dot the new dot. Upon some more research I found out that you can actually define types for class attributes before the `__init__()` function which is very helpful. With this, I updated the skeleton code to look like this:

```python
class Skeleton:
    # Defining parameters
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around

    def __init__(self, length):
        self.length = length    
        self.anchor = None      

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0)
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_child(Dot(id))
            current_dot = current_dot.child
```

..and my Dot code to be this:

```python
class Dot:
    id: int             # Position in the dot list
    child: 'Dot | None' # Child dot of this object

    def __init__(self, id):
        self.id = id 
        self.child = None
    
    def add_child(self, child):
        """Assign a child to this dot object"""
        self.child = child
```

This just means that even if I am multiple child objects into interating, I will still get the functions that a particular dot has as the type of the `child` object is known.

With this, I now wanted to create the distances between different dots. My current thinking is that the skeleton will have uniform distances between dots and that distance will be passed into the dots. Each dot will also track it's position and when constraining it's child dot, it will use it's position and adjust the child based on that (poorly explained but I'm figuring this one out myself).

```python
class Dot:
    id: int             # Position in the dot list
    child: 'Dot | None' # Child dot of this object
    dist: int           # Distance to constrain child to
    position: pygame.Vector2 # Current position of the dot

    def __init__(self, id, dist, pos):
        self.id = id 
        self.child = None
        self.dist = dist
        self.position = pos
```

With this I also changed the `Skeleton` code:

```python
class Skeleton:
    # Defining parameters
    length: int             # Length of the skeleton
    anchor: 'Dot | None'    # The dot that is moved around
    dot_dist: int

    def __init__(self, length, dist):
        self.length = length    
        self.anchor = None      
        self.dot_dist = dist

        self.setup_skeleton()

    def setup_skeleton(self):
        """Setup the full skeleton"""
        self.anchor = Dot(0, self.dot_dist, pygame.Vector2(0, 0))
        current_dot = self.anchor

        for id in range(1, self.length):
            current_dot.add_child(Dot(id, self.dot_dist, pygame.Vector2(current_dot.position.x + self.dot_dist, 0)))
            current_dot = current_dot.child
```

Just to add, because this is essentially a linked list, it allows for easy debugging just in the console without needing to have things showing on screen just yet. For example, to test that this functionality is working I wrote a simple linked-list traversal program to print the position of each dot:

```python
if __name__ == "__main__":
    skeleton = Skeleton(3, 50)
    current_dot = skeleton.anchor

    while current_dot != None:
        print(current_dot.position)
        current_dot = current_dot.child
```

This prints out "[0, 0] [50, 0] [100, 0]" which is exactly what we want to see. What I now want to do is move this into a constrain function rather than have the skeleton do it so we can get started on that piece of the functionality.

```python
def constrain_child(self):
    """Constrain the child to be in the radius defined in the skeleton"""
    self.child.position = self.position + pygame.Vector2(self.dist, 0)
```

Very basic functionality but it works so we can stick with it for now.

Next is to draw these dots to the screen which should be quite easy:

```python
def draw(self, screen):
    current_dot = self.anchor

    while current_dot != None:
        pygame.draw.circle(screen, (255, 255, 255), current_dot.position, 5, 3)
        current_dot = current_dot.child
```

And with this we can see our circles on the screen!

[^1]: [Argonaut's "A simple procedural animation technique"](https://www.youtube.com/watch?v=qlfh_rv6khY)
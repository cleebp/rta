import math

# The particle or planets or whatever are called shades in the code.
class Shade():
    # Initialize shade with a radius and centerpoint. Tuple expected by arg centerpoint.
    # Centerpoint is unused in this code, but I left it in because it could be used later.
    def __init__(self, radius, centerpoint):
        self.xCord, self.yCord = centerpoint
        self.radius = radius
        self.center = centerpoint

    # This lets shade change its own position.
    def updatePos(self, newX, newY):
        self.xCord = newX
        self.yCord = newY

    # This lets shade receive a tuple, unpack it, and update its position with it.
    def receiveCord(self, cords):
        x, y = cords
        self.updatePos(x, y)

    # This lets shade draw itself to the context. We're assuming
    # here that all shades are white, and want to be circles.
    # But further upgrades could change that. True for filled, False for outline.
    def drawSelf(self, context, fill):
        context.set_source_rgb(1, 1, 1)
        context.arc(self.xCord, self.yCord, self.radius, 0, 2 * math.pi)
        if fill == True:
            context.fill()
        else:
            context.stroke()
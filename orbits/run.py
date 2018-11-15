import cairo

from orbit import Orbit
from shade import Shade

FRAMECOUNT = 10


if __name__ == '__main__':
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    ctx = cairo.Context(surface)

    frames = FRAMECOUNT

    # Initial positions of Shades don't matter to the program.
    blackhole = Shade(125, (500, 500))
    planet = Shade(25, (800, 500))
    moon = Shade(5, (750, 500))

    # Find the planet's orbit around 500, 500, or our black hole.
    # And assign it to planetPos
    planetPos = Orbit(FRAMECOUNT, 300, (500, 500), 0)

    # animation
    for x in range(frames):
        # Blank the screen.
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, 1000, 1000)
        ctx.fill()

        # Update the positions. Recursion!
        planet.receiveCord(planetPos.finalCords[x])
        moonPos = Orbit(FRAMECOUNT, 50, planetPos.finalCords[x], x)
        moon.receiveCord(moonPos.finalCords[x])

        # Tell the planets to draw themselves.
        blackhole.drawSelf(ctx, False)
        planet.drawSelf(ctx, True)
        moon.drawSelf(ctx, False)

        # Draw the thing to a png, and iterate over however many frames.
        ctx.stroke()
        print('Creating Frame')
        surface.write_to_png('Frame' + str(x) + '.png')

    print('Finished')
import math

class Orbit():
    def __init__(self, frameCount, radius, center, phase):
        # Initializes Positions with the number of frames, a radius of
        # the orbit, a center of the orbit, and a phase. The phase is where
        # the planet starts in its orbit. At phase 0, the planet starts
        # at the far right and moves clockwise. Currently no ability to
        # make counter-clockwise.
        #
        # Takes the frame count and slices a circle into that many wedges,
        # then finds the x and y coordinate along a circle a unit circle and adds it
        # to a list.
        self.radian = 2 * math.pi / frameCount
        self.slices = []
        for x in range(frameCount):
            currentSlice = self.radian * x
            xVal = math.cos(currentSlice)
            yVal = math.sin(currentSlice)
            self.slices.append((xVal, yVal))
        # Scales those coordinates by the radius. Creates a new list filled with
        # tuples of the correctly scaled x, y coordinates.
        self.storedCords = []
        for each in self.slices:
            xVal = (each[0] * radius)
            yVal = (each[1] * radius)
            self.storedCords.append((xVal, yVal))
        # Translates those coordinates to the correct centerpoint inside the image.
        # Goes through each coordinate and makes a new tuple with correct translation.
        self.centerpoint = center
        xCent, yCent = center
        for i in range(len(self.storedCords)):
            tempX = self.storedCords[i][0] + xCent
            tempY = self.storedCords[i][1] + yCent
            self.storedCords[i] = (tempX, tempY)
            # A phase of 0 means the planet starts on the right side.
        # A phase of half your framecount starts it on the left side.
        # Simple slice and dice.
        self.finalCords = self.storedCords[phase:]
        for x in self.storedCords[:phase]:
            self.finalCords.append(x)
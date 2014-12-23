import Image
import math
import random

size = 512


class Layer:

    def __init__(self, json, container):
        self.container = container
        self.json = json
        self.name = json['name']
        self.type = json['type']
        self.alpha = float(json['transparency'])
        self.i = int(size)
        self.j = int(size)
        # create a new black image
        self.img = Image.new('RGB', (self.i, self.j), "black")
        self.pixels = self.img.load()

    def paint(self):
        print 'paint func'
        if self.type == 'background':
            self.background()
        elif self.type == 'stars':
            self.stars()
        elif self.type == 'masked_stars':
            self.masked_stars()
        elif self.type == 'correlated_stars':
            pass
        elif self.type == 'nebulae':
            pass
        elif self.type == 'billboard':
            pass
        elif self.type == 'temp':
            self.temp()
        else:
            print 'passed'

    def background(self):
        print 'background func'
        red = self.json['rgb'][0]
        green = self.json['rgb'][1]
        blue = self.json['rgb'][2]
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.pixels[i, j] = (red, green, blue)

    def stars(self):
        print 'stars func'

        density = float(self.json['density'])

        red_max = self.json['rgb_max'][0]
        green_max = self.json['rgb_max'][1]
        blue_max = self.json['rgb_max'][2]

        red_min = self.json['rgb_min'][0]
        green_min = self.json['rgb_min'][1]
        blue_min = self.json['rgb_min'][2]

        large = float(self.json['large_perc'])

        for i in range(self.img.size[0]):    # for every pixel:
            for j in range(self.img.size[1]):
                if(random.random() > density):
                    color = linint(
                        (red_max, green_max, blue_max), (red_min, green_min, blue_min), random.random())
                    if(random.random() > large):
                        self.pixels[i, j] = (
                            int(color[0]), int(color[1]), int(color[2]))
                    else:
                        self.pixels[i, j] = (
                            int(color[0]), int(color[1]), int(color[2]))
                        self.pixels[min(
                            self.img.size[0] - 1, i + 1), j] = (int(color[0]), int(color[1]), int(color[2]))
                        self.pixels[min(self.img.size[0] - 1, i + 1), min(self.img.size[1] - 1, j + 1)] = (
                            int(color[0]), int(color[1]), int(color[2]))
                        self.pixels[i, min(
                            self.img.size[1] - 1, j + 1)] = (int(color[0]), int(color[1]), int(color[2]))

    def masked_stars(self):
        print 'masked stars func'

        density = float(self.json['density'])
        print "reference is " + self.json['reference']
        reference = self.container[self.json['reference']]
        print "Found reference" + reference.name

        ref_vec = (	float(self.json['ref vector'][0]),
                    float(self.json['ref vector'][1]),
                    float(self.json['ref vector'][2])
                    )
        test = float(self.json['test'])

        red_max = self.json['rgb_max'][0]
        green_max = self.json['rgb_max'][1]
        blue_max = self.json['rgb_max'][2]

        red_min = self.json['rgb_min'][0]
        green_min = self.json['rgb_min'][1]
        blue_min = self.json['rgb_min'][2]

        large = float(self.json['large_perc'])

        for i in range(self.img.size[0]):    # for every pixel:
            for j in range(self.img.size[1]):
                if dot(ref_vec, reference.pixels[i, j]) > test:
                    if(random.random() > density):
                        color = linint(
                            (red_max, green_max, blue_max), (red_min, green_min, blue_min), random.random())
                        if(random.random() > large):
                            self.pixels[i, j] = (
                                int(color[0]), int(color[1]), int(color[2]))
                        else:
                            self.pixels[i, j] = (
                                int(color[0]), int(color[1]), int(color[2]))
                            self.pixels[min(
                                self.img.size[0] - 1, i + 1), j] = (int(color[0]), int(color[1]), int(color[2]))
                            self.pixels[min(self.img.size[0] - 1, i + 1), min(self.img.size[1] - 1, j + 1)] = (
                                int(color[0]), int(color[1]), int(color[2]))
                            self.pixels[i, min(
                                self.img.size[1] - 1, j + 1)] = (int(color[0]), int(color[1]), int(color[2]))

    def correlated_stars(self):
        print 'correlated_stars func'

    def nebulae(self):
        print 'correlated_stars func'

    def billboard(self):
        print 'billboard func'

    def temp(self):
        a = int(self.json['freq'])
        rgb_max = self.json['rgb_max']
        rgb_min = self.json['rgb_min']

        for i in range(self.img.size[0]):    # for every pixel:
            for j in range(self.img.size[1]):
                p = 1 + math.sin(a * 2 * math.pi * i / size)
                self.pixels[i, j] = (		 int(rgb_min[0] + p * (rgb_max[0] - rgb_min[0])), int(rgb_min[
                    1] + p * (rgb_max[1] - rgb_min[1])), int(rgb_min[2] + p * (rgb_max[2] - rgb_min[2])))

    def add(self, b):
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                if b.pixels[i, j] != (0, 0, 0):
                    self.pixels[i, j] = (	int(self.pixels[i, j][0] * b.alpha + b.pixels[i, j][0] * (1 - b.alpha)),
                                          int(self.pixels[i, j][
                                              1] * b.alpha + b.pixels[i, j][1] * (1 - b.alpha)),
                                          int(self.pixels[i, j][2] * b.alpha + b.pixels[i, j][2] * (1 - b.alpha)))


class LayerList:

    def __init__(self):
        self.list = []

    def __getitem__(self, key):
        result = None
        print "key is " + key
        for x in self.list:
            if x.name == key:
                result = x
        return result


# Helper functions
def linint(a, b, c):
    return (a[0] * (1 - c) + c * b[0],
            a[1] * (1 - c) + c * b[1],
            a[2] * (1 - c) + c * b[2])


def dot(a, b):
    return (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / (size * size)

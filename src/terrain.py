import enum
import pygame

class TerrainShape(enum.IntEnum):
    FLAT = 0
    SLOPE_W = 1
    SLOPE_S = 2
    SLOPE_E = 3
    SLOPE_N = 4
    FULL_SW = 5
    FULL_SE = 6
    FULL_NE = 7
    FULL_NW = 8
    UPPER_SW = 9
    UPPER_SE = 10
    UPPER_NE = 11
    UPPER_NW = 12
    LOWER_SW = 13
    LOWER_SE = 14
    LOWER_NE = 15
    LOWER_NW = 16
    FOLD_SW_NE = 17
    FOLD_SE_NW = 18
TS = TerrainShape

#SW, SE, NE, NW
SHAPE_BY_CORNER_HEIGHT = {
    ( 0, 0, 0, 0): (TS.FLAT, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),

    (-1, 1, 1,-1): (TS.SLOPE_W, 'CliffW', 'CliffS_W', 'CliffE', 'CliffN_W'),
    (-1,-1, 1, 1): (TS.SLOPE_S, 'CliffW_S', 'CliffS', 'CliffE_S', 'CliffN'),
    ( 1,-1,-1, 1): (TS.SLOPE_E, 'CliffW', 'CliffS_E', 'CliffE', 'CliffN_E'),
    ( 1, 1,-1,-1): (TS.SLOPE_N, 'CliffW_N', 'CliffS', 'CliffE_N', 'CliffN'),

    (-2, 0, 2, 0): (TS.FULL_SW, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 0,-2, 0, 2): (TS.FULL_SE, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 2, 0,-2, 0): (TS.FULL_NE, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 0, 2, 0,-2): (TS.FULL_NW, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),

    ( 0, 0, 2, 0): (TS.UPPER_SW, 'CliffW', 'CliffS', 'CliffE_S', 'CliffN_W'),
    ( 0, 0, 0, 2): (TS.UPPER_SE, 'CliffW_S', 'CliffS', 'CliffE', 'CliffN_E'),
    ( 2, 0, 0, 0): (TS.UPPER_NE, 'CliffW_N', 'CliffS_E', 'CliffE', 'CliffN'),
    ( 0, 2, 0, 0): (TS.UPPER_NW, 'CliffW', 'CliffS_W', 'CliffE_N', 'CliffN'),

    (-2, 0, 0, 0): (TS.LOWER_SW, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 0,-2, 0, 0): (TS.LOWER_SE, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 0, 0,-2, 0): (TS.LOWER_NE, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    ( 0, 0, 0,-2): (TS.LOWER_NW, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),

    ( 1,-1, 1,-1): (TS.FOLD_SW_NE, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
    (-1, 1,-1, 1): (TS.FOLD_SE_NW, 'CliffW', 'CliffS', 'CliffE', 'CliffN'),
}

ROTATED_SHAPES = [
    (TS.FLAT, TS.FLAT, TS.FLAT, TS.FLAT),
    (TS.SLOPE_W, TS.SLOPE_S, TS.SLOPE_E, TS.SLOPE_N),
    (TS.SLOPE_S, TS.SLOPE_E, TS.SLOPE_N, TS.SLOPE_W),
    (TS.SLOPE_E, TS.SLOPE_N, TS.SLOPE_W, TS.SLOPE_S),
    (TS.SLOPE_N, TS.SLOPE_W, TS.SLOPE_S, TS.SLOPE_E),
    (TS.FULL_SW, TS.FULL_SE, TS.FULL_NE, TS.FULL_NW),
    (TS.FULL_SE, TS.FULL_NE, TS.FULL_NW, TS.FULL_SW),
    (TS.FULL_NE, TS.FULL_NW, TS.FULL_SW, TS.FULL_SE),
    (TS.FULL_NW, TS.FULL_SW, TS.FULL_SE, TS.FULL_NE),
    (TS.UPPER_SW, TS.UPPER_SE, TS.UPPER_NE, TS.UPPER_NW),
    (TS.UPPER_SE, TS.UPPER_NE, TS.UPPER_NW, TS.UPPER_SW),
    (TS.UPPER_NE, TS.UPPER_NW, TS.UPPER_SW, TS.UPPER_SE),
    (TS.UPPER_NW, TS.UPPER_SW, TS.UPPER_SE, TS.UPPER_NE),
    (TS.LOWER_SW, TS.LOWER_SE, TS.LOWER_NE, TS.LOWER_NW),
    (TS.LOWER_SE, TS.LOWER_NE, TS.LOWER_NW, TS.LOWER_SW),
    (TS.LOWER_NE, TS.LOWER_NW, TS.LOWER_SW, TS.LOWER_SE),
    (TS.LOWER_NW, TS.LOWER_SW, TS.LOWER_SE, TS.LOWER_NE),
    (TS.FOLD_SW_NE, TS.FOLD_SE_NW, TS.FOLD_SW_NE, TS.FOLD_SE_NW),
    (TS.FOLD_SE_NW, TS.FOLD_SW_NE, TS.FOLD_SE_NW, TS.FOLD_SW_NE),
]

Y_OFFSET = [64, 48,48,48,48, 64,64,64,64, 64,64,64,64, 64,64,64,64, 48,48]

TERRAIN_MATERIALS = [
    ('grass', 'art/surface_grass.png'),
]

def load_assets():
    global images
    images = {}
    for name, fname in TERRAIN_MATERIALS:
        src = pygame.image.load(fname).convert_alpha()
        images[name] = [
            (src.subsurface(pygame.Rect(i*128, 0, 128, 128)), 64, Y_OFFSET[i])
            for i in range(len(TerrainShape))]


class TerrainElement:
    def __init__(self, terrain, east, north, corner_height=(0,0,0,0), material='grass'):
        self.terrain = terrain
        self.east = east
        self.north = north
        self.corner_height = list(corner_height) #SW, SE, NE, NW
        self.height = 0
        self.shape = None
        self.material = material
        self.cliffs = []

    def get_image(self, view_angle):
        return images[self.material][ROTATED_SHAPES[self.shape][view_angle]]

    def __str__(self):
        return f'{self.__class__.__name__}(east={self.east}, north={self.north}, shape={self.shape.name}, corner_height={self.corner_height})'

    def move_corner_up(self, corner):
        self.corner_height[corner] += 2
        h = self.corner_height[corner]
        for i, delta in ((-1, 2), (-2, 4), (-3, 2)):
            self.corner_height[corner + i] = max(h - delta, self.corner_height[corner + i])
        self.recalculate_propagate()

    def move_corner_down(self, corner):
        self.corner_height[corner] -= 2
        h = self.corner_height[corner]
        for i, delta in ((-1, 2), (-2, 4), (-3, 2)):
            self.corner_height[corner + i] = min(h + delta, self.corner_height[corner + i])
        self.recalculate_propagate()

    def move_up(self):
        h0 = min(self.corner_height)
        self.corner_height = [max(h, h0+2) for h in self.corner_height]
        self.recalculate_propagate()

    def move_down(self):
        h0 = max(self.corner_height)
        self.corner_height = [min(h, h0-2) for h in self.corner_height]
        self.recalculate_propagate()

    def recalculate_propagate(self):
        self.recalculate()
        if self.east > 0:
            self.terrain[self.east-1][self.north].recalculate()
        if self.east < len(self.terrain)-1:
            self.terrain[self.east+1][self.north].recalculate()
        if self.north > 0:
            self.terrain[self.east][self.north-1].recalculate()
        if self.north < len(self.terrain[self.east])-1:
            self.terrain[self.east][self.north+1].recalculate()

    def recalculate(self):
        div, mod = divmod(sum(self.corner_height), 8)
        self.height = 2*div + (0, None, 0, None, 1, None, 2, None)[mod]
        delta_height = tuple([ch - self.height for ch in self.corner_height])
        self.shape, *cliffs = SHAPE_BY_CORNER_HEIGHT[delta_height]
        self.cliffs = []
        #return
        for k in range(4):
            a = self.corner_height[k-1]
            b = self.corner_height[k]
            c = cliffs[k]
            (de,dn) = [(-1,0), (0,-1), (1,0), (0,1)][k]

            h = (a+b)//2

            if 0 <= self.east + de < len(self.terrain) and 0 <= self.north + dn < len(self.terrain[0]):
                neighbour = self.terrain[self.east + de][self.north + dn]
                dh = max(a - neighbour.corner_height[k-2], b - neighbour.corner_height[k-3])
            else:
                dh = max(a + 20, b + 20)

            if dh > 0:
                self.cliffs.append((c, h))
                h = 2*(h//2)
            for h0 in range(h-4, h-dh, -4):
                if dh == 0:
                    self.cliffs.append((c, h0))
                else:
                    self.cliffs.append((c[:6], h0))

def create_sample_terrain():
    terrain = s = []
    terrain.extend([
        [TerrainElement(terrain,0,0,(-2,-2,-2,-2)), TerrainElement(terrain,0,1), TerrainElement(terrain,0,2), TerrainElement(terrain,0,3), TerrainElement(terrain,0,4), TerrainElement(terrain,0,5,(0,0,0,2))],
        [TerrainElement(terrain,1,0), TerrainElement(terrain,1,1), TerrainElement(terrain,1,2), TerrainElement(terrain,1,3), TerrainElement(terrain,1,4), TerrainElement(terrain,1,5,(0,2,2,0))],
        [TerrainElement(terrain,2,0), TerrainElement(terrain,2,1,(0,0,2,0)), TerrainElement(terrain,2,2,(0,2,2,0)), TerrainElement(terrain,2,3), TerrainElement(terrain,2,4), TerrainElement(terrain,2,5,(2,4,4,2))],
        [TerrainElement(terrain,3,0), TerrainElement(terrain,3,1,(0,0,2,2)), TerrainElement(terrain,3,2,(2,2,2,2)), TerrainElement(terrain,3,3,(0,2,2,0)), TerrainElement(terrain,3,4), TerrainElement(terrain,3,5,(4,6,6,4))],
        [TerrainElement(terrain,4,0), TerrainElement(terrain,4,1,(0,0,2,2)), TerrainElement(terrain,4,2,(2,2,2,2)), TerrainElement(terrain,4,3,(2,2,2,2)), TerrainElement(terrain,4,4), TerrainElement(terrain,4,5,(6,6,6,6))],
        [TerrainElement(terrain,5,0), TerrainElement(terrain,5,1,(0,0,0,2)), TerrainElement(terrain,5,2,(2,0,0,2)), TerrainElement(terrain,5,3,(2,0,0,2)), TerrainElement(terrain,5,4), TerrainElement(terrain,5,5,(6,4,4,6))],
        [TerrainElement(terrain,6,0), TerrainElement(terrain,6,1), TerrainElement(terrain,6,2,(4,4,4,4)), TerrainElement(terrain,6,3), TerrainElement(terrain,6,4), TerrainElement(terrain,6,5,(4,2,2,4))],
        [TerrainElement(terrain,7,0,(0,2,0,0)), TerrainElement(terrain,7,1), TerrainElement(terrain,7,2), TerrainElement(terrain,7,3), TerrainElement(terrain,7,4), TerrainElement(terrain,7,5,(2,0,0,2))],
    ])

    for tr in terrain:
        for tr in tr:
            tr.recalculate()
    return terrain

terrain = create_sample_terrain()

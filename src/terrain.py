import enum
import pygame

class Subtiles(enum.IntEnum):
    SW = 0
    SE = 1
    NE = 2
    NW = 3

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
    NUMBER_OF_IMAGES = 19
TS = TerrainShape

class WallShape(enum.IntEnum):
    WALL_W_S = 0
    WALL_S_W = 1
    WALL_W = 2
    WALL_S = 3
    WALL_W_N = 4
    WALL_S_E = 5
    FRONT = 6
    WALL_E_N = 6
    WALL_N_E = 7
    WALL_E = 8
    WALL_N = 9
    WALL_E_S = 10
    WALL_N_W = 11
    NUMBER_OF_IMAGES = 12

WS = WallShape

#SW, SE, NE, NW
SHAPE_BY_CORNER_HEIGHT = {
    ( 0, 0, 0, 0): (TS.FLAT, WS.WALL_W, WS.WALL_S, WS.WALL_E, WS.WALL_N),

    (-1, 1, 1,-1): (TS.SLOPE_W, WS.WALL_W, WS.WALL_S_W, WS.WALL_E, WS.WALL_N_W),
    (-1,-1, 1, 1): (TS.SLOPE_S, WS.WALL_W_S, WS.WALL_S, WS.WALL_E_S, WS.WALL_N),
    ( 1,-1,-1, 1): (TS.SLOPE_E, WS.WALL_W, WS.WALL_S_E, WS.WALL_E, WS.WALL_N_E),
    ( 1, 1,-1,-1): (TS.SLOPE_N, WS.WALL_W_N, WS.WALL_S, WS.WALL_E_N, WS.WALL_N),

    (-2, 0, 2, 0): (TS.FULL_SW, WS.WALL_W_S, WS.WALL_S_W, WS.WALL_E_S, WS.WALL_N_W),
    ( 0,-2, 0, 2): (TS.FULL_SE, WS.WALL_W_S, WS.WALL_S_E, WS.WALL_E_S, WS.WALL_N_E),
    ( 2, 0,-2, 0): (TS.FULL_NE, WS.WALL_W_N, WS.WALL_S_E, WS.WALL_E_N, WS.WALL_N_E),
    ( 0, 2, 0,-2): (TS.FULL_NW, WS.WALL_W_N, WS.WALL_S_W, WS.WALL_E_N, WS.WALL_N_W),

    ( 0, 0, 2, 0): (TS.UPPER_SW, WS.WALL_W, WS.WALL_S, WS.WALL_E_S, WS.WALL_N_W),
    ( 0, 0, 0, 2): (TS.UPPER_SE, WS.WALL_W_S, WS.WALL_S, WS.WALL_E, WS.WALL_N_E),
    ( 2, 0, 0, 0): (TS.UPPER_NE, WS.WALL_W_N, WS.WALL_S_E, WS.WALL_E, WS.WALL_N),
    ( 0, 2, 0, 0): (TS.UPPER_NW, WS.WALL_W, WS.WALL_S_W, WS.WALL_E_N, WS.WALL_N),

    (-2, 0, 0, 0): (TS.LOWER_SW, WS.WALL_W_S, WS.WALL_S_W, WS.WALL_E, WS.WALL_N),
    ( 0,-2, 0, 0): (TS.LOWER_SE, WS.WALL_W, WS.WALL_S_E, WS.WALL_E_S, WS.WALL_N),
    ( 0, 0,-2, 0): (TS.LOWER_NE, WS.WALL_W, WS.WALL_S, WS.WALL_E_N, WS.WALL_N_E),
    ( 0, 0, 0,-2): (TS.LOWER_NW, WS.WALL_W_N, WS.WALL_S, WS.WALL_E, WS.WALL_N_W),

    ( 1,-1, 1,-1): (TS.FOLD_SW_NE, WS.WALL_W_N, WS.WALL_S_E, WS.WALL_E_S, WS.WALL_N_W),
    (-1, 1,-1, 1): (TS.FOLD_SE_NW, WS.WALL_W_S, WS.WALL_S_W, WS.WALL_E_N, WS.WALL_N_E),
}


ROTATED_SHAPES_SURFACE = [
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

ROTATED_SHAPES_WALLS = [
    (WS.WALL_W_S, WS.WALL_S_E, None, None),
    (WS.WALL_S_W, None, None, WS.WALL_W_N),
    (WS.WALL_W, WS.WALL_S, WS.WALL_E, WS.WALL_N),
    (WS.WALL_S, WS.WALL_E, WS.WALL_N, WS.WALL_W),
    (WS.WALL_W_N, WS.WALL_S_W, None, None),
    (WS.WALL_S_E, None, None, WS.WALL_W_S),

    (None, None, WS.WALL_W_S, WS.WALL_S_E),
    (None, WS.WALL_W_N, WS.WALL_S_W, None),
    (WS.WALL_E, WS.WALL_N, WS.WALL_W, WS.WALL_S),
    (WS.WALL_N, WS.WALL_W, WS.WALL_S, WS.WALL_E),
    (None, None, WS.WALL_W_N, WS.WALL_S_W),
    (None, WS.WALL_W_S, WS.WALL_S_E, None),
]

WALL_EXTENSION = [
    WS.WALL_W, WS.WALL_S, WS.WALL_W, WS.WALL_S, WS.WALL_W, WS.WALL_S,
    WS.WALL_E, WS.WALL_N, WS.WALL_E, WS.WALL_N, WS.WALL_E, WS.WALL_N,
]


SURFACE_SPECIALS = [
    ('_subtile', 'art/surface_masks.png', 0),
    ('_border', 'art/surface_border.png', 0),
    (('_corner', Subtiles.SW), 'art/surface_markings.png', 0),
    (('_corner', Subtiles.SE), 'art/surface_markings.png', 128),
    (('_corner', Subtiles.NE), 'art/surface_markings.png', 256),
    (('_corner', Subtiles.NW), 'art/surface_markings.png', 384),
]

SURFACE_MATERIALS = [
    ('grass', 'art/surface_grass.png', 0),
    ('water', 'art/surface_water.png', 0),
]

WALL_MATERIALS = [
    ('dirt', 'art/cliff_dirt.png'),
    ('waterfall', 'art/cliff_waterfall.png'),
]

def load_assets():
    Y_OFFSET = [64, 48,48,48,48, 64,64,64,64, 64,64,64,64, 64,64,64,64, 48,48]
    X_OFFSET = [64, 0, 64, 0, 64, 0, 64, 0, 64, 0, 64, 0]
    global images
    images = {}
    for name, fname, y in SURFACE_SPECIALS:
        src = pygame.image.load(fname).convert_alpha()
        images[name] = [
            (src.subsurface(pygame.Rect(i*128, y, 128, 128)), 64, Y_OFFSET[i])
            for i in range(TerrainShape.NUMBER_OF_IMAGES)]

    for name, fname, y in SURFACE_MATERIALS:
        src = pygame.image.load(fname).convert_alpha()
        images[name, False] = [
            (src.subsurface(pygame.Rect(i*128, y, 128, 128)), 64, Y_OFFSET[i])
            for i in range(TerrainShape.NUMBER_OF_IMAGES)]
        src = src.copy()
        border = images['_border'][0][0].get_abs_parent()
        border = border.copy()
        border.fill((0,0,0,128), special_flags=pygame.BLEND_RGBA_MULT)
        src.blit(border, (0,0))
        images[name, True] = [
            (src.subsurface(pygame.Rect(i*128, y, 128, 128)), 64, Y_OFFSET[i])
            for i in range(TerrainShape.NUMBER_OF_IMAGES)]

    for name, fname in WALL_MATERIALS:
        src = pygame.image.load(fname).convert_alpha()
        images[name] = [
            (src.subsurface(pygame.Rect(i*64, 0, 64, 144)), X_OFFSET[i], 32)
            for i in range(WallShape.NUMBER_OF_IMAGES)]


class TerrainElement:
    def __init__(self, terrain, east, north, corner_height=(0,0,0,0), surf_material='grass', wall_material='dirt'):
        self.terrain = terrain
        self.east = east
        self.north = north
        self.corner_height = list(corner_height) #SW, SE, NE, NW
        self.height = 0
        self.shape = None
        self.surf_material = surf_material
        self.wall_material = wall_material
        self.walls = []
        self.selected = False
        self.selected_corner = None

    def get_surface_image(self, view):
        img = images[self.surf_material, view.show_grid][ROTATED_SHAPES_SURFACE[self.shape][view.angle]]
        if self.selected:
            surf, x, y = img
            surf = surf.copy()
            surf.blit(images['_border'][ROTATED_SHAPES_SURFACE[self.shape][view.angle]][0], (0,0))
            if self.selected_corner is not None:
                surf.blit(images['_corner', (self.selected_corner+view.angle)%4][ROTATED_SHAPES_SURFACE[self.shape][view.angle]][0], (0,0))
            img = surf, x, y
        return img

    def get_wall_images_and_height(self, view):
        for wall, height, is_top in self.walls:
            if ROTATED_SHAPES_WALLS[wall][view.angle] is not None:
                if ROTATED_SHAPES_WALLS[wall][view.angle] < WS.FRONT or is_top:
                    yield images[self.wall_material][ROTATED_SHAPES_WALLS[wall][view.angle]], height

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
        self.shape, *walls = SHAPE_BY_CORNER_HEIGHT[delta_height]
        self.walls = []
        #return
        for k in range(4):
            a = self.corner_height[k-1]
            b = self.corner_height[k]
            c = walls[k]
            (de,dn) = [(-1,0), (0,-1), (1,0), (0,1)][k]

            h = (a+b)//2

            if 0 <= self.east + de < len(self.terrain) and 0 <= self.north + dn < len(self.terrain[0]):
                neighbour = self.terrain[self.east + de][self.north + dn]
                dh = max(a - neighbour.corner_height[k-2], b - neighbour.corner_height[k-3])
            else:
                dh = max(a + 20, b + 20)

            if dh > 0:
                self.walls.append((c, h, True))
                h = 2*(h//2)
            for h0 in range(h-4, h-dh, -4):
                self.walls.append((WALL_EXTENSION[c], h0, False))

    def subtile_at_pos(self, view, pos):
         subtile,_,_ = images['_subtile'][ROTATED_SHAPES_SURFACE[self.shape][view.angle]]
         px = subtile.get_at(pos)
         if px[3]:
             return {
                (0,0):     [Subtiles.SW, Subtiles.SE, Subtiles.NE, Subtiles.NW][-view.angle],
                (255,0):   [Subtiles.SE, Subtiles.NE, Subtiles.NW, Subtiles.SW][-view.angle],
                (255,255): [Subtiles.NE, Subtiles.NW, Subtiles.SW, Subtiles.SE][-view.angle],
                (0,255):   [Subtiles.NW, Subtiles.SW, Subtiles.SE, Subtiles.NE][-view.angle],
             }.get((px[0], px[1]), None)

def create_sample_terrain():
    terrain = s = []
    terrain.extend([
        [TerrainElement(terrain,0,0,(-2,-2,-2,-2), 'water', 'waterfall'), TerrainElement(terrain,0,1), TerrainElement(terrain,0,2), TerrainElement(terrain,0,3), TerrainElement(terrain,0,4), TerrainElement(terrain,0,5,(0,0,0,2))],
        [TerrainElement(terrain,1,0,(0,0,0,0), 'water', 'waterfall'), TerrainElement(terrain,1,1), TerrainElement(terrain,1,2), TerrainElement(terrain,1,3), TerrainElement(terrain,1,4), TerrainElement(terrain,1,5,(0,2,2,0))],
        [TerrainElement(terrain,2,0,(0,0,0,0), 'water', 'waterfall'), TerrainElement(terrain,2,1,(0,0,2,0)), TerrainElement(terrain,2,2,(0,2,2,0)), TerrainElement(terrain,2,3), TerrainElement(terrain,2,4), TerrainElement(terrain,2,5,(2,4,4,2))],
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

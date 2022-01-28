import math
from dataclasses import dataclass
import pygame

TILE_WIDTH = 64
Z_OFFSET = 16

VIEW_FROM_SW = 0
VIEW_FROM_NW = 1
VIEW_FROM_NE = 2
VIEW_FROM_SE = 3

IMAGES = {
    'hillW': ('art/surface_grass.png', 64, 48, 1*128, 0, 128, 128),
    'hillS': ('art/surface_grass.png', 64, 48, 2*128, 0, 128, 128),
    'hillE': ('art/surface_grass.png', 64, 48, 3*128, 0, 128, 128),
    'hillN': ('art/surface_grass.png', 64, 48, 4*128, 0, 128, 128),
    'grass': ('art/surface_grass.png', 64, 64, 0*128, 0, 128, 128),
    'hillSE': ('art/surface_grass.png', 64, 64, 10*128, 0, 128, 128),
    'hillNE': ('art/surface_grass.png', 64, 64, 11*128, 0, 128, 128),
    'hillNW': ('art/surface_grass.png', 64, 64, 12*128, 0, 128, 128),
    'hillSW': ('art/surface_grass.png', 64, 64, 9*128, 0, 128, 128),

    'cliffW':   ('art/cliff_dirt.png', 64, 16, 128, 0, 64, 128),
    'cliffS':   ('art/cliff_dirt.png',  0, 16, 192, 0, 64, 128),
    'cliffW_S': ('art/cliff_dirt.png', 64, 16,   0, 0, 64, 128),
    'cliffS_W': ('art/cliff_dirt.png',  0, 16,  64, 0, 64, 128),
    'cliffW_N': ('art/cliff_dirt.png', 64, 16, 256, 0, 64, 128),
    'cliffS_E': ('art/cliff_dirt.png',  0, 16, 320, 0, 64, 128),

    'trkNS': ('art/models/track/0000.png', 64, 32, 0, 0, 128, 64),
    'trkEW': ('art/models/track/0001.png', 64, 32, 0, 0, 128, 64),

    'trk2NE_00': ('art/models/track/0002.png', 64, 32, 0, 0, 128, 64),
    'trk2NE_01': ('art/models/track/0003.png', 64, 32, 0, 0, 128, 64),
    'trk2NE_10': ('art/models/track/0004.png', 64, 32, 0, 0, 128, 64),
    'trk2NE_11': ('art/models/track/0005.png', 64, 32, 0, 0, 128, 64),

    'trk2NW_00': ('art/models/track/0006.png', 64, 32, 0, 0, 128, 64),
    'trk2NW_01': ('art/models/track/0007.png', 64, 32, 0, 0, 128, 64),
    'trk2NW_10': ('art/models/track/0008.png', 64, 32, 0, 0, 128, 64),
    'trk2NW_11': ('art/models/track/0009.png', 64, 32, 0, 0, 128, 64),

    'trk2SE_00': ('art/models/track/0010.png', 64, 32, 0, 0, 128, 64),
    'trk2SE_01': ('art/models/track/0011.png', 64, 32, 0, 0, 128, 64),
    'trk2SE_10': ('art/models/track/0012.png', 64, 32, 0, 0, 128, 64),
    'trk2SE_11': ('art/models/track/0013.png', 64, 32, 0, 0, 128, 64),

    'trk2SW_00': ('art/models/track/0014.png', 64, 32, 0, 0, 128, 64),
    'trk2SW_01': ('art/models/track/0015.png', 64, 32, 0, 0, 128, 64),
    'trk2SW_10': ('art/models/track/0016.png', 64, 32, 0, 0, 128, 64),
    'trk2SW_11': ('art/models/track/0017.png', 64, 32, 0, 0, 128, 64),

    }
for i in range(24):
    IMAGES[f'lok{i:02d}'] = (f'art/models/lok/{i:04d}.png', 192, 96, 0, 0, 384, 192)


TILES = {
    'Grass': ['grass', 'grass', 'grass', 'grass'],
    'GrassW': ['hillW', 'hillS', 'hillE', 'hillN'],
    'GrassS': ['hillS', 'hillE', 'hillN', 'hillW'],
    'GrassE': ['hillE', 'hillN', 'hillW', 'hillS'],
    'GrassN': ['hillN', 'hillW', 'hillS', 'hillE'],
    'GrassSW': ['hillSW', 'hillSE', 'hillNE', 'hillNW'],
    'GrassSE': ['hillSE', 'hillNE', 'hillNW', 'hillSW'],
    'GrassNE': ['hillNE', 'hillNW', 'hillSW', 'hillSE'],
    'GrassNW': ['hillNW', 'hillSW', 'hillSE', 'hillNE'],

    'CliffW': ['cliffW', 'cliffS', None, None],
    'CliffS': ['cliffS', None, None, 'cliffW'],
    'CliffE': [None, None, 'cliffW', 'cliffS'],
    'CliffN': [None, 'cliffW', 'cliffS', None],

    'CliffW_S': ['cliffW_S', 'cliffS_E', None, None],
    'CliffS_E': ['cliffS_E', None, None, 'cliffW_S'],
    'CliffE_N': [None, None, 'cliffW_S', 'cliffS_E'],
    'CliffN_W': [None, 'cliffW_S', 'cliffS_E', None],

    'CliffW_N': ['cliffW_N', 'cliffS_W', None, None],
    'CliffS_W': ['cliffS_W', None, None, 'cliffW_N'],
    'CliffE_S': [None, None, 'cliffW_N', 'cliffS_W'],
    'CliffN_E': [None, 'cliffW_N', 'cliffS_W', None],

    'TrkNS': ['trkNS', 'trkEW', 'trkNS', 'trkEW'],
    'TrkEW': ['trkEW', 'trkNS', 'trkEW', 'trkNS'],


    'Trk2NE_00': ['trk2NE_00', 'trk2NW_01', 'trk2SW_11', 'trk2SE_10'],
    'Trk2NE_01': ['trk2NE_01', 'trk2NW_11', 'trk2SW_10', 'trk2SE_00'],
    'Trk2NE_10': ['trk2NE_10', 'trk2NW_00', 'trk2SW_01', 'trk2SE_11'],
    'Trk2NE_11': ['trk2NE_11', 'trk2NW_10', 'trk2SW_00', 'trk2SE_01'],

    'Trk2NW_00': ['trk2NW_00', 'trk2SW_01', 'trk2SE_11', 'trk2NE_10'],
    'Trk2NW_01': ['trk2NW_01', 'trk2SW_11', 'trk2SE_10', 'trk2NE_00'],
    'Trk2NW_10': ['trk2NW_10', 'trk2SW_00', 'trk2SE_01', 'trk2NE_11'],
    'Trk2NW_11': ['trk2NW_11', 'trk2SW_10', 'trk2SE_00', 'trk2NE_01'],

    'Trk2SW_00': ['trk2SW_00', 'trk2SE_01', 'trk2NE_11', 'trk2NW_10'],
    'Trk2SW_01': ['trk2SW_01', 'trk2SE_11', 'trk2NE_10', 'trk2NW_00'],
    'Trk2SW_10': ['trk2SW_10', 'trk2SE_00', 'trk2NE_01', 'trk2NW_11'],
    'Trk2SW_11': ['trk2SW_11', 'trk2SE_10', 'trk2NE_00', 'trk2NW_01'],

    'Trk2SE_00': ['trk2SE_00', 'trk2NE_01', 'trk2NW_11', 'trk2SW_10'],
    'Trk2SE_01': ['trk2SE_01', 'trk2NE_11', 'trk2NW_10', 'trk2SW_00'],
    'Trk2SE_10': ['trk2SE_10', 'trk2NE_00', 'trk2NW_01', 'trk2SW_11'],
    'Trk2SE_11': ['trk2SE_11', 'trk2NE_10', 'trk2NW_00', 'trk2SW_01'],
}

SPRITES = {
    'lok': [f'lok{i:02d}' for i in range(24)]
}

tiles = [  # S -----> N       W v E
    [[('Grass', -2), ('CliffW', -2), ('CliffS', -2)],   [('Grass', 0), ('CliffS', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0), ('CliffN', 0)],   ],
    [[('Grass', 0), ('CliffW', 0), ('CliffS', 0), ('Trk2NE_00', 0)],   [('Grass', 0), ('Trk2NE_10', 0)],   [('Grass', 0), ('TrkNS', 0)],   [('Grass', 0), ('Trk2SE_00', 0)],   [('Grass', 0), ('Trk2SE_10', 0)],   [('GrassW', 1), ('CliffN_W', 1), ('CliffS_W', 1)],   ],
    [[('Grass', 0), ('CliffS', 0), ('Trk2NE_01', 0)],   [('GrassSW', 0), ('Trk2NE_11', 0)], [('GrassW', 1), ('CliffN_W', 1)],  [('Grass', 0), ('Trk2SE_01', 0)],   [('Grass', 0), ('Trk2SE_11', 0)],   [('GrassW', 3), ('CliffN_W', 3), ('CliffS_W', 3)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0)],   [('GrassS', 1)],  [('Grass', 2), ('CliffN', 2)],   [('GrassW', 1)],  [('Grass', 0), ('TrkEW', 0)], [('GrassW', 5), ('CliffN_W', 5), ('CliffS_W', 5)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0)],   [('GrassS', 1)],  [('Grass', 2)],   [('Grass', 2), ('CliffE', 2)],   [('Grass', 0), ('TrkEW', 0)],  [('Grass', 6), ('CliffN', 6), ('CliffS', 6), ('CliffS', 2)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0)],   [('GrassSE', 0)], [('GrassE', 1)],  [('GrassE', 1), ('CliffE_S', 1)],  [('Grass', 0), ('TrkEW', 0)], [('GrassE', 5), ('CliffN_E', 5), ('CliffS_E', 5)],   ],
    [[('Grass', 0), ('CliffS', 0), ('Trk2NW_00', 0)],   [('Grass', 0), ('Trk2NW_10', 0)],   [('Grass', 0)],   [('Grass', 0), ('Trk2SW_00', 0)],   [('Grass', 0), ('Trk2SW_10', 0)],   [('GrassE', 3), ('CliffN_E', 3), ('CliffS_E', 3)],   ],
    [[('Grass', 0), ('CliffS', 0), ('CliffE', 0), ('Trk2NW_01', 0)],   [('Grass', 0), ('CliffE', 0), ('Trk2NW_11', 0)],   [('Grass', 0), ('CliffE', 0), ('TrkNS', 0)],   [('Grass', 0), ('CliffE', 0), ('Trk2SW_01', 0)],   [('Grass', 0), ('CliffE', 0), ('Trk2SW_11', 0)],   [('GrassE', 1), ('CliffE', 0), ('CliffN_E', 1), ('CliffS_E', 1)],   ],
]

@dataclass
class Sprite:
    stype: str
    east: float
    north: float
    z: float
    rot: float

    def get_image(self, view_rot):
        sheet = SPRITES[self.stype]
        n = len(sheet)
        k = int(self.rot * n / (2 * math.pi) + view_rot * n/4 + 0.5) % n
        return sheet[k]


TRACK_PIECES = [
    ('WE', 1, lambda s: (s, 0.5)),
    ('2WN', math.pi * 0.75, lambda s: (s, 0.5)),
]


def car_pos(s):
    pi, sin, cos = math.pi, math.sin, math.cos

    A = 3
    B = 3 + 0.75*pi
    C = 4 + 0.75*pi
    D = 4 + 1.50*pi
    E = 7 + 1.50*pi
    F = 7 + 2.25*pi
    G = 8 + 2.25*pi
    L = 8 + 3.00*pi

    s %= L

    if 0 <= s < A:
        return (3 + s, 0.5, 0)
    elif A <= s < B:
        phi = (s - A) / 1.5
        return (6 + 1.5 * sin(phi), 2 - 1.5 * cos(phi), phi)
    elif B <= s < C:
        return (7.5, 2 + s - B, pi/2)
    elif C <= s < D:
        phi = (s - C) / 1.5 + pi/2
        return (6 + 1.5 * sin(phi), 3 - 1.5 * cos(phi), phi)
    elif D <= s < E:
        return (6 - s + D, 4.5, pi)
    elif E <= s < F:
        phi = (s - E) / 1.5 + pi
        return (3 + 1.5 * sin(phi), 3 - 1.5 * cos(phi), phi)
    elif F <= s < G:
        return (1.5, 3 - s + F, pi*1.5)
    else:
        phi = (s - G) / 1.5 + pi * 1.5
        return (3 + 1.5 * sin(phi), 2 - 1.5 * cos(phi), phi)




sprites = [
    Sprite('lok', 3.5, 0.5, 0, 0)
]

MAP_SIZE_NS = 6
MAP_SIZE_EW = 8

LAYER_FRONT = 1
LAYER_SURFACE = 2


@dataclass
class View:
    angle: int
    x_offset: int
    y_offset: int

    def en_from_uv(self,u,v):
        if self.angle == VIEW_FROM_SW:
            e = MAP_SIZE_EW - u
            n = MAP_SIZE_NS - v
        elif self.angle == VIEW_FROM_NW:
            e = MAP_SIZE_EW - v
            n = u
        elif self.angle == VIEW_FROM_NE:
            e = u
            n = v
        elif self.angle == VIEW_FROM_SE:
            e = v
            n = MAP_SIZE_NS - u
        return e,n

    def uv_from_en(self,e,n):
        if self.angle == VIEW_FROM_SW:
            u = MAP_SIZE_EW - e
            v = MAP_SIZE_NS - n
        elif self.angle == VIEW_FROM_NW:
            v = MAP_SIZE_EW - e
            u = n
        elif self.angle == VIEW_FROM_NE:
            u = e
            v = n
        elif self.angle == VIEW_FROM_SE:
            v = e
            u = MAP_SIZE_NS - n
        return u,v

    def rotate(self, cx, cy):
        u = (2 * cy - cx - 2*self.y_offset + self.x_offset)/(2*TILE_WIDTH)
        v = (2 * cy + cx - 2*self.y_offset - self.x_offset)/(2*TILE_WIDTH)

        e, n = self.en_from_uv(u, v)
        self.angle = (self.angle + 1) % 4
        u, v = self.uv_from_en(e, n)

        self.x_offset = int(cx - TILE_WIDTH*(v-u))
        self.y_offset = int(cy - TILE_WIDTH*(u+v)/2)


def load_assets():
    source_surfs = {}
    global images
    images = {}
    for name, (fname, dx, dy, sx, sy, sw, sh) in IMAGES.items():
        if fname in source_surfs:
            src = source_surfs[fname]
        else:
            src = pygame.image.load(fname).convert_alpha()
            source_surfs[fname] = src
        images[name] = (src.subsurface(pygame.Rect(sx, sy, sw, sh)), dx, dy)


s = 0

def update(dt):
    global s
    s += dt
    sprites[0].east, sprites[0].north, sprites[0].rot = car_pos(s)

def blits(view: View, sel_pos):
    if sel_pos is not None:
        sel_x, sel_y = sel_pos
    else:
        sel_x = sel_y = -1

    selected_blit = None
    if view.angle == VIEW_FROM_SW or view.angle == VIEW_FROM_NE:
        U = MAP_SIZE_EW
        V = MAP_SIZE_NS
    else:
        U = MAP_SIZE_NS
        V = MAP_SIZE_EW
    for u in range(U):
        for v in range(V):
            e,n = view.en_from_uv(u+0.5, v+0.5)
            for tile, h in tiles[int(e)][int(n)]:
                rot_tile = TILES[tile][view.angle]
                if not rot_tile:
                    continue
                surf, dx, dy = images[rot_tile]
                x = view.x_offset + TILE_WIDTH * (v-u) - dx
                y = view.y_offset + TILE_WIDTH * (u+v+1)//2 - h*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                sw, sh = surf.get_size()
                if sel_pos is not None and x <= sel_x < x+sw and y <= sel_y < y+sh:
                    pixel = surf.get_at((sel_x - x, sel_y - y))
                    if pixel[3]:
                        # not completely transparent
                        selected_blit = (surf, x, y)
                yield surf, (x, y)
            # use some kind of index in order only to select sprites on the tile
            for sprite in sprites:
                if int(e) <= sprite.east < int(e)+1 and int(n) <= sprite.north < int(n)+1:
                    rot_tile = sprite.get_image(view.angle)
                    if not rot_tile:
                        continue
                    us, vs = view.uv_from_en(sprite.east, sprite.north)
                    surf, dx, dy = images[rot_tile]
                    x = int(view.x_offset + TILE_WIDTH * (vs-us) - dx)
                    y = int(view.y_offset + TILE_WIDTH * (us+vs)//2 - sprite.z*Z_OFFSET - dy)

                    sw, sh = surf.get_size()
                    if sel_pos is not None and x <= sel_x < x+sw and y <= sel_y < y+sh:
                        pixel = surf.get_at((sel_x - x, sel_y - y))
                        if pixel[3]:
                            # not completely transparent
                            selected_blit = (surf, x, y)
                    yield surf, (x, y)

    if selected_blit:
        surf, x, y = selected_blit
        ghost = surf.copy()
        ghost.fill((128,128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
        ghost.fill((192,192,192), special_flags=pygame.BLEND_ADD)
        yield ghost, (x, y)

import math
from dataclasses import dataclass
from collections import defaultdict
import pygame

TILE_HALF_WIDTH = 64
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

    'mask_1': ('art/spritemask.png', 64, 92, 0, 0, 128, 128),
    'mask_2SW': ('art/spritemask.png', 64, 92, 1*128, 0, 128, 128),
    'mask_2SE': ('art/spritemask.png', 64, 92, 2*128, 0, 128, 128),
    'mask_2NE': ('art/spritemask.png', 64, 92, 3*128, 0, 128, 128),
    'mask_2NW': ('art/spritemask.png', 64, 92, 4*128, 0, 128, 128),
    'mask_4SW': ('art/spritemask.png', 64, 92, 5*128, 0, 128, 128),
    'mask_4SE': ('art/spritemask.png', 64, 92, 6*128, 0, 128, 128),
    'mask_4NE': ('art/spritemask.png', 64, 92, 7*128, 0, 128, 128),
    'mask_4NW': ('art/spritemask.png', 64, 92, 8*128, 0, 128, 128),
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

    'Mask_1': ['mask_1', 'mask_1', 'mask_1', 'mask_1'],
    'Mask_2SW': ['mask_2SW', 'mask_2SE', 'mask_2NE', 'mask_2NW'],
    'Mask_2SE': ['mask_2SE', 'mask_2NE', 'mask_2NW', 'mask_2SW'],
    'Mask_2NE': ['mask_2NE', 'mask_2NW', 'mask_2SW', 'mask_2SE'],
    'Mask_2NW': ['mask_2NW', 'mask_2SW', 'mask_2SE', 'mask_2NE'],
    'Mask_4SW': ['mask_4SW', 'mask_4SE', 'mask_4NE', 'mask_4NW'],
    'Mask_4SE': ['mask_4SE', 'mask_4NE', 'mask_4NW', 'mask_4SW'],
    'Mask_4NE': ['mask_4NE', 'mask_4NW', 'mask_4SW', 'mask_4SE'],
    'Mask_4NW': ['mask_4NW', 'mask_4SW', 'mask_4SE', 'mask_4NE'],

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
    [[('Grass', 0), ('CliffW', 0), ('CliffS', 0), ('Trk2NE_00', 0, 11)],   [('Grass', 0), ('Trk2NE_10', 0, 11)],   [('Grass', 0), ('TrkNS', 0, 10)],   [('Grass', 0), ('Trk2SE_00', 0, 9)],   [('Grass', 0), ('Trk2SE_10', 0, 9)],   [('GrassW', 1), ('CliffN_W', 1), ('CliffS_W', 1)],   ],
    [[('Grass', 0), ('CliffS', 0), ('Trk2NE_01', 0, 11)],   [('GrassSW', 0), ('Trk2NE_11', 0, 11)], [('GrassW', 1), ('CliffN_W', 1)],  [('Grass', 0), ('Trk2SE_01', 0, 9)],   [('Grass', 0), ('Trk2SE_11', 0, 9)],   [('GrassW', 3), ('CliffN_W', 3), ('CliffS_W', 3)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0, 0)],   [('GrassS', 1)],  [('Grass', 2), ('CliffN', 2)],   [('GrassW', 1)],  [('Grass', 0), ('TrkEW', 0, 8)], [('GrassW', 5), ('CliffN_W', 5), ('CliffS_W', 5)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0, 1)],   [('GrassS', 1)],  [('Grass', 2)],   [('Grass', 2), ('CliffE', 2)],   [('Grass', 0), ('TrkEW', 0, 7)],  [('Grass', 6), ('CliffN', 6), ('CliffS', 6), ('CliffS', 2)],   ],
    [[('Grass', 0), ('CliffS', 0), ('TrkEW', 0, 2)],   [('GrassSE', 0)], [('GrassE', 1)],  [('GrassE', 1), ('CliffE_S', 1)],  [('Grass', 0), ('TrkEW', 0, 6)], [('GrassE', 5), ('CliffN_E', 5), ('CliffS_E', 5)],   ],
    [[('Grass', 0), ('CliffS', 0), ('Trk2NW_00', 0, 3)],   [('Grass', 0), ('Trk2NW_10', 0, 3)],   [('Grass', 4), ('CliffN', 4), ('CliffS', 4), ('CliffW', 4), ('CliffE', 4), ('TrkNS', 4)],   [('Grass', 0), ('Trk2SW_00', 0, 5), ('TrkNS', 4)],   [('Grass', 0), ('Trk2SW_10', 0, 5), ('TrkNS', 4)],   [('GrassE', 3), ('CliffN_E', 3), ('CliffS_E', 3), ('TrkNS', 4)],   ],
    [[('Grass', 0), ('CliffS', 0), ('CliffE', 0), ('Trk2NW_01', 0, 3)],   [('Grass', 0), ('CliffE', 0), ('Trk2NW_11', 0, 3)],   [('Grass', 0), ('CliffE', 0), ('TrkNS', 0, 4)],   [('Grass', 0), ('CliffE', 0), ('Trk2SW_01', 0, 5)],   [('Grass', 0), ('CliffE', 0), ('Trk2SW_11', 0, 5)],   [('GrassE', 1), ('CliffE', 0), ('CliffN_E', 1), ('CliffS_E', 1)],   ],
]

@dataclass
class Sprite:
    stype: str
    east: float
    north: float
    z: float
    rot: float

    def __hash__(self):
        return hash(id(self))

    def get_image(self, view_rot):
        sheet = SPRITES[self.stype]
        n = len(sheet)
        k = int(self.rot * n / (2 * math.pi) + view_rot * n/4 + 0.5) % n
        return sheet[k]


TRACK_PIECES = {
    'WE': (1, lambda s: (s-0.5, 0, 0)),
    'SN': (1, lambda s: (0, s-0.5, math.pi * 0.5)),
    'EW': (1, lambda s: (0.5-s, 0, math.pi)),
    'NS': (1, lambda s: (0, 0.5-s, math.pi * 1.5)),

    '2WN': (math.pi * 0.75, lambda s: (-1 + 1.5 * math.sin(s/1.5),  1 - 1.5 * math.cos(s/1.5), s/1.5)),
    '2SW': (math.pi * 0.75, lambda s: (-1 + 1.5 * math.cos(s/1.5), -1 + 1.5 * math.sin(s/1.5), s/1.5 + math.pi * 0.5)),
    '2ES': (math.pi * 0.75, lambda s: ( 1 - 1.5 * math.sin(s/1.5), -1 + 1.5 * math.cos(s/1.5), s/1.5 + math.pi)),
    '2NE': (math.pi * 0.75, lambda s: ( 1 - 1.5 * math.cos(s/1.5),  1 - 1.5 * math.sin(s/1.5), s/1.5 + math.pi * 1.5)),
}

class Car:
    pass

car = Car()
car.track_index = 0
car.track_pos = 0

class Ride:
    pass

ride = Ride()
ride.name = 'Wild West Train'
ride.track = [
    (3.5, 0.5, 0, 'WE',  [(3,0,'TrkEW','Mask_1')]),
    (4.5, 0.5, 0, 'WE',  [(4,0,'TrkEW','Mask_1')]),
    (5.5, 0.5, 0, 'WE',  [(5,0,'TrkEW','Mask_1')]),
    (7,   1,   0, '2WN', [(6,0,'Trk2NW_00', 'Mask_1'), (7,0,'Trk2NW_01', 'Mask_2NW'), (6,1,'Trk2NW_10', 'Mask_4SE'), (7,1,'Trk2NW_11', 'Mask_1')]),
    (7.5, 2.5, 0, 'SN',  [(7,2,'TrkNS','Mask_1')]),
    (7,   4,   0, '2SW', [(7,3,'Trk2SW_01', 'Mask_1'), (7,4,'Trk2SW_11', 'Mask_2SW'), (6,3,'Trk2SW_00', 'Mask_4NE'), (6,4,'Trk2SW_10', 'Mask_1')]),
    (5.5, 4.5, 0, 'EW',  [(5,4,'TrkEW','Mask_1')]),
    (4.5, 4.5, 0, 'EW',  [(4,4,'TrkEW','Mask_1')]),
    (3.5, 4.5, 0, 'EW',  [(3,4,'TrkEW','Mask_1')]),
    (2,   4,   0, '2ES', [(2,4,'Trk2SE_11', 'Mask_1'), (1,4,'Trk2SE_10', 'Mask_2SE'), (2,3,'Trk2SE_01', 'Mask_4NW'), (1,3,'Trk2SE_00', 'Mask_1')]),
    (1.5, 2.5, 0, 'NS',  [(1,2,'TrkNS','Mask_1')]),
    (2,   1,   0, '2NE', [(1,1,'Trk2NE_10', 'Mask_1'), (1,0,'Trk2NE_00', 'Mask_2NE'), (2,1,'Trk2NE_11', 'Mask_4SW'), (2,0,'Trk2NE_01', 'Mask_1')]),
]
ride.cars = [car]
ride.cars_on_track = [set() for _ in ride.track]
car.ride = ride
car.sprite = Sprite('lok', 3.5, 0.5, 0, 0)


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
        u = (2 * cy - cx - 2*self.y_offset + self.x_offset)/(2*TILE_HALF_WIDTH)
        v = (2 * cy + cx - 2*self.y_offset - self.x_offset)/(2*TILE_HALF_WIDTH)

        e, n = self.en_from_uv(u, v)
        self.angle = (self.angle + 1) % 4
        u, v = self.uv_from_en(e, n)

        self.x_offset = int(cx - TILE_HALF_WIDTH*(v-u))
        self.y_offset = int(cy - TILE_HALF_WIDTH*(u+v)/2)


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


def update(dt):
    car.track_pos += 2*dt

    tp = TRACK_PIECES[car.ride.track[car.track_index][3]]
    while car.track_pos > tp[0]:
        car.track_pos -= tp[0]
        car.track_index = (car.track_index + 1) % len(car.ride.track)
        tp = TRACK_PIECES[car.ride.track[car.track_index][3]]

    e,n,r = tp[1](car.track_pos)
    e += car.ride.track[car.track_index][0]
    n += car.ride.track[car.track_index][1]

    car.sprite.east, car.sprite.north, car.sprite.rot = e,n,r


def masked_blit(src, x, y, mask, xm, ym):
    '''create a masked version of the source and return a blitting spec'''
    src_w, src_h = src.get_size()
    tmp = mask.copy()
    tmp.blit(src, (x-xm, y-ym), special_flags=pygame.BLEND_RGBA_MULT)
    tmp_w, tmp_h = tmp.get_size()
    tmp_rect = pygame.Rect(0, 0, tmp_w, tmp_h)
    src_rect = tmp_rect.clip(pygame.Rect(x - xm, y - ym, src_w, src_h))
    if src_rect.width and src_rect.height:
        return tmp.subsurface(src_rect), (xm + src_rect.left, ym + src_rect.top)

class Selector:
    def __init__(self, sel_pos):
        self.x = sel_pos[0]
        self.y = sel_pos[1]
        self.selected = None

    def check(self, surf, x, y):
        sw, sh = surf.get_size()
        if x <= self.x < x+sw and y <= self.y < y+sh:
            pixel = surf.get_at((self.x - x, self.y - y))
            if pixel[3]: # not completely transparent
                self.selected = (surf, (x, y))

    def ghost(self):
        if self.selected:
            surf, (x, y) = self.selected
            ghost = surf.copy()
            ghost.fill((128,128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
            ghost.fill((192,192,192), special_flags=pygame.BLEND_ADD)
            yield ghost, (x, y)

class DummySelector:
    def check(self, surf, x, y):
        pass
    def ghost(self):
        return []


def blits(view: View, sel_pos):
    if sel_pos is not None:
        selector = Selector(sel_pos)
    else:
        selector = DummySelector()

    if view.angle == VIEW_FROM_SW or view.angle == VIEW_FROM_NE:
        U = MAP_SIZE_EW
        V = MAP_SIZE_NS
    else:
        U = MAP_SIZE_NS
        V = MAP_SIZE_EW
    for u in range(U):
        for v in range(V):
            e,n = view.en_from_uv(u+0.5, v+0.5)
            for t in tiles[int(e)][int(n)]:
                tile, h = t[0], t[1]
                if not(tile.startswith('Trk') and h==0):
                    rot_tile = TILES[tile][view.angle]
                    if not rot_tile:
                        continue
                    surf, dx, dy = images[rot_tile]
                    x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                    y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                    selector.check(surf, x, y)
                    yield surf, (x, y)
                else:
                    track_index = t[2]
                    (_,_,h,_,pcs) = ride.track[track_index]
                    for (ee,nn,tile,mask) in pcs:
                        if ee == int(e) and nn==int(n):
                            rot_tile = TILES[tile][view.angle]
                            if not rot_tile:
                                continue
                            surf, dx, dy = images[rot_tile]
                            x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                            y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                            selector.check(surf, x, y)
                            yield surf, (x, y)

                            prep_sprites = []
                            for car in ride.cars:
                                if (car.track_index - track_index + 1) % len(ride.track) > 2:
                                    continue
                                rot_tile = car.sprite.get_image(view.angle)
                                if not rot_tile:
                                    continue
                                us, vs = view.uv_from_en(car.sprite.east, car.sprite.north)
                                surf, dx, dy = images[rot_tile]
                                x = int(view.x_offset + TILE_HALF_WIDTH * (vs-us) - dx)
                                y = int(view.y_offset + TILE_HALF_WIDTH * (us+vs)//2 - car.sprite.z*Z_OFFSET - dy)

                                # clip to mask for the given tile
                                rot_mask = TILES[mask][view.angle]
                                mask, dmx, dmy = images[rot_mask]
                                xm = int(view.x_offset + TILE_HALF_WIDTH * (v-u) - dmx)
                                ym = int(view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h*Z_OFFSET - dmy)

                                masked = masked_blit(surf, x, y, mask, xm, ym)
                                if masked:
                                    surf, (x, y) = masked
                                    selector.check(surf, x, y)
                                    yield surf, (x, y)
    yield from selector.ghost()

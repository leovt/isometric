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

    'surfmW': ('art/surface_masks.png', 64, 48, 1*128, 0, 128, 128),
    'surfmS': ('art/surface_masks.png', 64, 48, 2*128, 0, 128, 128),
    'surfmE': ('art/surface_masks.png', 64, 48, 3*128, 0, 128, 128),
    'surfmN': ('art/surface_masks.png', 64, 48, 4*128, 0, 128, 128),
    'surfm': ('art/surface_masks.png', 64, 64, 0*128, 0, 128, 128),
    'surfmSE': ('art/surface_masks.png', 64, 64, 10*128, 0, 128, 128),
    'surfmNE': ('art/surface_masks.png', 64, 64, 11*128, 0, 128, 128),
    'surfmNW': ('art/surface_masks.png', 64, 64, 12*128, 0, 128, 128),
    'surfmSW': ('art/surface_masks.png', 64, 64, 9*128, 0, 128, 128),

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
    def __init__(self, ride, sprite):
        self.track_element = ride.track[0]
        self.track_pos = 0
        self.ride = ride
        self.sprite = sprite
        self.update(0)

    def __str__(self):
        return f'Car({self.ride}, {self.sprite}, {self.track_element})'

    def update(self, dt):
        self.track_pos += 2*dt

        tp = TRACK_PIECES[self.track_element.track_piece]
        while self.track_pos > tp[0]:
            self.track_pos -= tp[0]
            self.track_element = self.track_element.next
            tp = TRACK_PIECES[self.track_element.track_piece]

        e,n,r = tp[1](self.track_pos)
        e += self.track_element.east
        n += self.track_element.north

        self.sprite.east, self.sprite.north, self.sprite.rot = e,n,r

TILE_BY_CORNER_HEIGHT = {
    (0,0,0,0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'),

    ( 1, 1,-1,-1): ('GrassN', 'CliffW_N', 'CliffS', 'CliffE_N', 'CliffN'),
    (-1, 1, 1,-1): ('GrassW', 'CliffW', 'CliffS_W', 'CliffE', 'CliffN_W'),
    (-1,-1, 1, 1): ('GrassS', 'CliffW_S', 'CliffS', 'CliffE_S', 'CliffN'),
    ( 1,-1,-1, 1): ('GrassE', 'CliffW', 'CliffS_E', 'CliffE', 'CliffN_E'),

    ( 1,-1, 1,-1): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo
    (-1, 1,-1, 1): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo

    ( 2, 0, 0, 0): ('GrassNE', 'CliffW_N', 'CliffS_E', 'CliffE', 'CliffN'),
    ( 0, 2, 0, 0): ('GrassNW', 'CliffW', 'CliffS_W', 'CliffE_N', 'CliffN'),
    ( 0, 0, 2, 0): ('GrassSW', 'CliffW', 'CliffS', 'CliffE_S', 'CliffN_W'),
    ( 0, 0, 0, 2): ('GrassSE', 'CliffW_S', 'CliffS', 'CliffE', 'CliffN_E'),

    (-2, 0, 0, 0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #'GrassSWd',
    ( 0,-2, 0, 0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #'GrassSEd',
    ( 0, 0,-2, 0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #'GrassNEd',
    ( 0, 0, 0,-2): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #'GrassNWd',

    ( 2, 0,-2, 0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo
    ( 0, 2, 0,-2): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo
    (-2, 0, 2, 0): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo
    ( 0,-2, 0, 2): ('Grass', 'CliffW', 'CliffS', 'CliffE', 'CliffN'), #todo
}

class TerrainElement:
    def __init__(self, terrain, east, north, corner_height=(0,0,0,0)):
        self.terrain = terrain
        self.east = east
        self.north = north
        self.corner_height = list(corner_height) #SW, SE, NE, NW
        self.height = 0
        self.tile = None
        self.cliffs = []

    def __str__(self):
        return f'{self.__class__.__name__}(east={self.east}, north={self.north}, tile={self.tile}, corner_height={self.corner_height})'

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
        self.tile, *cliffs = TILE_BY_CORNER_HEIGHT[delta_height]
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


@dataclass
class RideTrackElement:
    ride: object
    east: float
    north: float
    height: int
    track_piece: str
    subpieces: list
    next: object=None
    prev: object=None

    def __str__(self):
        return f'RideTrackElement({self.ride}, east={self.east}, north={self.north}, track={self.track_piece})'

class Ride:
    def update(self, dt):
        for car in self.cars:
            car.update(dt)

    def __str__(self):
        return f'Ride(name={self.name})'

ride = Ride()
ride.name = 'Wild West Train'
ride.track = [
    RideTrackElement(ride, 3.5, 0.5, 0, 'WE',  [(3,0,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 4.5, 0.5, 0, 'WE',  [(4,0,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 5.5, 0.5, 0, 'WE',  [(5,0,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 7,   1,   0, '2WN', [(6,0,'Trk2NW_00', 'Mask_1'), (7,0,'Trk2NW_01', 'Mask_2NW'), (6,1,'Trk2NW_10', 'Mask_4SE'), (7,1,'Trk2NW_11', 'Mask_1')]),
    RideTrackElement(ride, 7.5, 2.5, 0, 'SN',  [(7,2,'TrkNS','Mask_1')]),
    RideTrackElement(ride, 7,   4,   0, '2SW', [(7,3,'Trk2SW_01', 'Mask_1'), (7,4,'Trk2SW_11', 'Mask_2SW'), (6,3,'Trk2SW_00', 'Mask_4NE'), (6,4,'Trk2SW_10', 'Mask_1')]),
    RideTrackElement(ride, 5.5, 4.5, 0, 'EW',  [(5,4,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 4.5, 4.5, 0, 'EW',  [(4,4,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 3.5, 4.5, 0, 'EW',  [(3,4,'TrkEW','Mask_1')]),
    RideTrackElement(ride, 2,   4,   0, '2ES', [(2,4,'Trk2SE_11', 'Mask_1'), (1,4,'Trk2SE_10', 'Mask_2SE'), (2,3,'Trk2SE_01', 'Mask_4NW'), (1,3,'Trk2SE_00', 'Mask_1')]),
    RideTrackElement(ride, 1.5, 2.5, 0, 'NS',  [(1,2,'TrkNS','Mask_1')]),
    RideTrackElement(ride, 2,   1,   0, '2NE', [(1,1,'Trk2NE_10', 'Mask_1'), (1,0,'Trk2NE_00', 'Mask_2NE'), (2,1,'Trk2NE_11', 'Mask_4SW'), (2,0,'Trk2NE_01', 'Mask_1')]),

    RideTrackElement(ride, 6.5, 2.5, 4, 'SN',  [(6,2,'TrkNS','Mask_1')]),
    RideTrackElement(ride, 6.5, 3.5, 4, 'SN',  [(6,3,'TrkNS','Mask_1')]),
    RideTrackElement(ride, 6.5, 4.5, 4, 'SN',  [(6,4,'TrkNS','Mask_1')]),
    RideTrackElement(ride, 6.5, 5.5, 4, 'SN',  [(6,5,'TrkNS','Mask_1')]),
]

for a,b in zip(ride.track[0:12], ride.track[1:12] + ride.track[0:1]):
    a.next = b
    b.prev = a
for a,b in zip(ride.track[12:15], ride.track[13:16]):
    a.next = b
    b.prev = a


ride.cars = [Car(ride, Sprite('lok', 3.5, 0.5, 0, 0))]
ride.cars_on_track = [set() for _ in ride.track]

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
del tr

worldmap = [  # S -----> N       W v E
    [[('TERRAIN',)],   [('TERRAIN',)],   [('TERRAIN',)],   [('TERRAIN',)],   [('TERRAIN',)],   [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 11)],   [('TERRAIN',), ('TRACK', ride, 11)],   [('TERRAIN',), ('TRACK', ride, 10)],   [('TERRAIN',), ('TRACK', ride, 9)],   [('TERRAIN',), ('TRACK', ride, 9)],   [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 11)],   [('TERRAIN',), ('TRACK', ride, 11)], [('TERRAIN',)],  [('TERRAIN',), ('TRACK', ride, 9)],   [('TERRAIN',), ('TRACK', ride, 9)],   [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 0)],   [('TERRAIN',)],  [('TERRAIN',)],   [('TERRAIN',)],  [('TERRAIN',), ('TRACK', ride, 8)], [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 1)],   [('TERRAIN',)],  [('TERRAIN',)],   [('TERRAIN',)],   [('TERRAIN',), ('TRACK', ride, 7)],  [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 2)],   [('TERRAIN',)], [('TERRAIN',)],  [('TERRAIN',)],  [('TERRAIN',), ('TRACK', ride, 6)], [('TERRAIN',)],   ],
    [[('TERRAIN',), ('TRACK', ride, 3)],   [('TERRAIN',), ('TRACK', ride, 3)],   [('TERRAIN',), ('TRACK', ride, 12)],   [('TERRAIN',), ('TRACK', ride, 5), ('TRACK', ride, 13)],   [('TERRAIN',), ('TRACK', ride, 5), ('TRACK', ride, 14)],   [('TERRAIN',), ('TRACK', ride, 15)],   ],
    [[('TERRAIN',), ('TRACK', ride, 3)],   [('TERRAIN',), ('TRACK', ride, 3)],   [('TERRAIN',), ('TRACK', ride, 4)],   [('TERRAIN',), ('TRACK', ride, 5)],   [('TERRAIN',), ('TRACK', ride, 5)],   [('TERRAIN',)],   ],
]

rides = [ride]
del ride

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
    for ride in rides:
        ride.update(dt)

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
        self.e = None
        self.n = None
        self.info = None
        self.mask_pixel = None

    def details(self):
        return f'position: {self.x},{self.y}\nelement: {self.info}\nmask: {self.mask_pixel}'

    def check(self, surf, x, y, e, n, info, mask=None):
        sw, sh = surf.get_size()
        if x <= self.x < x+sw and y <= self.y < y+sh:
            pixel = surf.get_at((self.x - x, self.y - y))
            if pixel[3]: # not completely transparent
                self.selected = (surf, (x, y))
                self.e = e
                self.n = n
                self.info = info
                if mask:
                    self.mask_pixel = mask.get_at((self.x - x, self.y - y))
                else:
                    self.mask_pixel = None


    def ghost(self):
        if self.selected:
            surf, (x, y) = self.selected
            ghost = surf.copy()
            ghost.fill((128,128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
            ghost.fill((192,192,192), special_flags=pygame.BLEND_ADD)
            yield ghost, (x, y)

class DummySelector:
    def check(self, *args):
        pass
    def ghost(self):
        return []


def blits(view: View, selector=None):
    if selector is None:
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
            terr = terrain[int(e)][int(n)]

            for t in worldmap[int(e)][int(n)]:
                t_type = t[0]
                if t_type == 'TERRAIN':
                    tile, h0 = terr.tile, terr.height
                    rot_tile = TILES[tile][view.angle]
                    if not rot_tile:
                        continue
                    surf, dx, dy = images[rot_tile]
                    x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                    y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h0*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                    if rot_tile == 'grass':
                        mask = 'surfm'
                    else:
                        mask = 'surfm' + rot_tile[4:]

                    selector.check(surf, x, y, int(e), int(n), terr, images[mask][0])
                    yield surf, (x, y)

                    for tile, h0 in terr.cliffs:
                        rot_tile = TILES[tile][view.angle]
                        if not rot_tile:
                            continue
                        surf, dx, dy = images[rot_tile]
                        x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                        y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h0*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                        selector.check(surf, x, y, int(e), int(n), terr)
                        yield surf, (x, y)


                elif t_type == 'TILE':
                    tile, h = t[1], t[2]
                    rot_tile = TILES[tile][view.angle]
                    if not rot_tile:
                        continue
                    surf, dx, dy = images[rot_tile]
                    x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                    y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - h*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                    selector.check(surf, x, y, int(e), int(n), t)
                    yield surf, (x, y)
                elif t_type == 'TRACK':
                    ride = t[1]
                    track_index = t[2]
                    rtp = ride.track[track_index]
                    for (ee,nn,tile,mask) in rtp.subpieces:
                        if ee == int(e) and nn==int(n):
                            rot_tile = TILES[tile][view.angle]
                            if not rot_tile:
                                continue
                            surf, dx, dy = images[rot_tile]
                            x = view.x_offset + TILE_HALF_WIDTH * (v-u) - dx
                            y = view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - rtp.height*Z_OFFSET - dy  #+1 because the tile is actually at u+0.5, v+0.5

                            selector.check(surf, x, y, int(e), int(n), rtp)
                            yield surf, (x, y)

                            prep_sprites = []
                            element = ride.track[track_index]
                            for car in ride.cars:
                                if not (element is car.track_element or element is car.track_element.next or element is car.track_element.prev):
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
                                ym = int(view.y_offset + TILE_HALF_WIDTH * (u+v+1)//2 - rtp.height*Z_OFFSET - dmy)

                                masked = masked_blit(surf, x, y, mask, xm, ym)
                                if masked:
                                    surf, (x, y) = masked
                                    selector.check(surf, x, y, int(e), int(n), car)
                                    yield surf, (x, y)
    yield from selector.ghost()

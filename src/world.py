import pygame

TILE_WIDTH = 50
Z_OFFSET = 15

VIEW_FROM_SW = 0
VIEW_FROM_NW = 1
VIEW_FROM_NE = 2
VIEW_FROM_SE = 3

IMAGES = {
    'hillW': ('art/roadTiles_nova/png/hillW.png', 50, 65),
    'hillS': ('art/roadTiles_nova/png/hillS.png', 50, 65),
    'hillE': ('art/roadTiles_nova/png/hillE.png', 50, 50),
    'hillN': ('art/roadTiles_nova/png/hillN.png', 50, 50),
    'grass': ('art/roadTiles_nova/png/grass.png', 50, 50),
    'hillSE': ('art/roadTiles_nova/png/hillES.png', 50, 50),
    'hillNE': ('art/roadTiles_nova/png/hillNE_corr.png', 50, 50),
    'hillNW': ('art/roadTiles_nova/png/hillNW.png', 50, 50),
    'hillSW': ('art/roadTiles_nova/png/hillSW.png', 50, 65),
    }

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
}

Map = [  # S -----> N       W v E
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
    [('Grass', 0),   ('GrassSW', 0), ('GrassW', 0),  ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
    [('Grass', 0),   ('GrassS', 0),  ('Grass', 1),   ('GrassW', 0),  ('GrassNW', 0), ('Grass', 0),   ],
    [('Grass', 0),   ('GrassS', 0),  ('Grass', 1),   ('Grass', 1),   ('GrassN', 0),  ('Grass', 0),   ],
    [('Grass', 0),   ('GrassSE', 0), ('GrassE', 0),  ('GrassE', 0),  ('GrassNE', 0), ('Grass', 0),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
]

MAP_SIZE_NS = 6
MAP_SIZE_EW = 8

def load_assets():
    global images
    images = { name: (pygame.image.load(fname).convert_alpha(), dx, dy)
        for (name, (fname, dx, dy)) in IMAGES.items()}

def blits(view_angle):
    if view_angle == VIEW_FROM_SW or view_angle == VIEW_FROM_NE:
        U = MAP_SIZE_EW
        V = MAP_SIZE_NS
    else:
        U = MAP_SIZE_NS
        V = MAP_SIZE_EW
    for u in range(U):
        for v in range(V):
            if view_angle == VIEW_FROM_SW:
                e = MAP_SIZE_EW - 1 - u
                n = MAP_SIZE_NS - 1 - v
            elif view_angle == VIEW_FROM_NW:
                e = MAP_SIZE_EW - 1 - v
                n = u
            elif view_angle == VIEW_FROM_NE:
                e = u
                n = v
            elif view_angle == VIEW_FROM_SE:
                e = v
                n = MAP_SIZE_NS - 1 - u

            tile, h = Map[e][n]
            surf, dx, dy = images[TILES[tile][view_angle]]
            yield surf, (500+TILE_WIDTH*(v-u)-dx, 100+TILE_WIDTH*(u+v)//2-h*Z_OFFSET-dy)

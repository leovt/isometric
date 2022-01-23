from dataclasses import dataclass
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
    [('Grass', -1),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('GrassW', 0),   ],
    [('Grass', 0),   ('GrassSW', 0), ('GrassW', 0),  ('Grass', 0),   ('Grass', 0),   ('GrassW', 1),   ],
    [('Grass', 0),   ('GrassS', 0),  ('Grass', 1),   ('GrassW', 0),  ('GrassNW', 0), ('GrassW', 2),   ],
    [('Grass', 0),   ('GrassS', 0),  ('Grass', 1),   ('Grass', 1),   ('GrassN', 0),  ('Grass', 3),   ],
    [('Grass', 0),   ('GrassSE', 0), ('GrassE', 0),  ('GrassE', 0),  ('GrassNE', 0), ('GrassE', 2),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('GrassE', 1),   ],
    [('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('Grass', 0),   ('GrassE', 0),   ],
]

MAP_SIZE_NS = 6
MAP_SIZE_EW = 8

@dataclass
class View:
    angle: int
    x_offset: int
    y_offset: int

    def en_from_uv(self,u,v):
        if self.angle == VIEW_FROM_SW:
            e = MAP_SIZE_EW - 1 - u
            n = MAP_SIZE_NS - 1 - v
        elif self.angle == VIEW_FROM_NW:
            e = MAP_SIZE_EW - 1 - v
            n = u
        elif self.angle == VIEW_FROM_NE:
            e = u
            n = v
        elif self.angle == VIEW_FROM_SE:
            e = v
            n = MAP_SIZE_NS - 1 - u
        return e,n

    def uv_from_en(self,e,n):
        if self.angle == VIEW_FROM_SW:
            u = MAP_SIZE_EW - 1 - e
            v = MAP_SIZE_NS - 1 - n
        elif self.angle == VIEW_FROM_NW:
            v = MAP_SIZE_EW - 1 - e
            u = n
        elif self.angle == VIEW_FROM_NE:
            u = e
            v = n
        elif self.angle == VIEW_FROM_SE:
            v = e
            u = MAP_SIZE_NS - 1 - n
        return u,v

    def rotate(self, cx, cy):
         u = (2 * cy - cx - 2*self.y_offset + self.x_offset)/(2*TILE_WIDTH)
         v = (2 * cy + cx - 2*self.y_offset - self.x_offset)/(2*TILE_WIDTH)

         e, n = self.en_from_uv(u, v)
         print((u,v), (e,n))
         self.angle = (self.angle + 1) % 4
         u, v = self.uv_from_en(e, n)

         self.x_offset = int(cx - TILE_WIDTH*(v-u))
         self.y_offset = int(cy - TILE_WIDTH*(u+v)/2)

def load_assets():
    global images
    images = { name: (pygame.image.load(fname).convert_alpha(), dx, dy)
        for (name, (fname, dx, dy)) in IMAGES.items()}

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
            e,n = view.en_from_uv(u,v)
            tile, h = Map[e][n]
            surf, dx, dy = images[TILES[tile][view.angle]]
            x = view.x_offset + TILE_WIDTH * (v-u) - dx
            y = view.y_offset + TILE_WIDTH * (u+v)//2 - h*Z_OFFSET - dy
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
        ghost.fill((128,128,128), special_flags=pygame.BLEND_MULT)
        ghost.fill((128,128,128), special_flags=pygame.BLEND_ADD)
        yield ghost, (x, y)

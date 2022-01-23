from dataclasses import dataclass
import pygame

TILE_WIDTH = 64
Z_OFFSET = 16

VIEW_FROM_SW = 0
VIEW_FROM_NW = 1
VIEW_FROM_NE = 2
VIEW_FROM_SE = 3

IMAGES = {
    'hillW': ('art/surface_grass.png', 64, 80, 1*128, 0, 128, 128),
    'hillS': ('art/surface_grass.png', 64, 80, 2*128, 0, 128, 128),
    'hillE': ('art/surface_grass.png', 64, 80, 3*128, 0, 128, 128),
    'hillN': ('art/surface_grass.png', 64, 80, 4*128, 0, 128, 128),
    'grass': ('art/surface_grass.png', 64, 96, 0*128, 0, 128, 128),
    'hillSE': ('art/surface_grass.png', 64, 96, 10*128, 0, 128, 128),
    'hillNE': ('art/surface_grass.png', 64, 96, 11*128, 0, 128, 128),
    'hillNW': ('art/surface_grass.png', 64, 96, 12*128, 0, 128, 128),
    'hillSW': ('art/surface_grass.png', 64, 96, 9*128, 0, 128, 128),

    'cliffW':   ('art/cliff_dirt.png', 64, 48, 128, 0, 64, 128),
    'cliffS':   ('art/cliff_dirt.png',  0, 48, 192, 0, 64, 128),
    'cliffW_S': ('art/cliff_dirt.png', 64, 48,   0, 0, 64, 128),
    'cliffS_W': ('art/cliff_dirt.png',  0, 48,  64, 0, 64, 128),
    'cliffW_N': ('art/cliff_dirt.png', 64, 48, 256, 0, 64, 128),
    'cliffS_E': ('art/cliff_dirt.png',  0, 48, 320, 0, 64, 128),
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
}

tiles = [  # S -----> N       W v E
    [[('Grass', -2), ('CliffW', -2), ('CliffS', -2)],   [('Grass', 0), ('CliffS', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0)],   [('Grass', 0), ('CliffW', 0), ('CliffN', 0)],   ],
    [[('Grass', 0), ('CliffW', 0), ('CliffS', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('GrassW', 1), ('CliffN_W', 1), ('CliffS_W', 1)],   ],
    [[('Grass', 0), ('CliffS', 0)],   [('GrassSW', 0)], [('GrassW', 1), ('CliffN_W', 1)],  [('Grass', 0)],   [('Grass', 0)],   [('GrassW', 3), ('CliffN_W', 3), ('CliffS_W', 3)],   ],
    [[('Grass', 0), ('CliffS', 0)],   [('GrassS', 1)],  [('Grass', 2), ('CliffN', 2)],   [('GrassW', 1)],  [('GrassNW', 0)], [('GrassW', 5), ('CliffN_W', 5), ('CliffS_W', 5)],   ],
    [[('Grass', 0), ('CliffS', 0)],   [('GrassS', 1)],  [('Grass', 2)],   [('Grass', 2)],   [('GrassN', 1)],  [('Grass', 6), ('CliffN', 6), ('CliffS', 6), ('CliffS', 2)],   ],
    [[('Grass', 0), ('CliffS', 0)],   [('GrassSE', 0)], [('GrassE', 1)],  [('GrassE', 1)],  [('GrassNE', 0)], [('GrassE', 5), ('CliffN_E', 5), ('CliffS_E', 5)],   ],
    [[('Grass', 0), ('CliffS', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('Grass', 0)],   [('GrassE', 3), ('CliffN_E', 3), ('CliffS_E', 3)],   ],
    [[('Grass', 0), ('CliffS', 0), ('CliffE', 0)],   [('Grass', 0), ('CliffE', 0)],   [('Grass', 0), ('CliffE', 0)],   [('Grass', 0), ('CliffE', 0)],   [('Grass', 0), ('CliffE', 0)],   [('GrassE', 1), ('CliffE', 0), ('CliffN_E', 1), ('CliffS_E', 1)],   ],
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
            for tile, h in tiles[e][n]:
                rot_tile = TILES[tile][view.angle]
                if not rot_tile:
                    continue
                surf, dx, dy = images[rot_tile]
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
        ghost.fill((128,128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
        ghost.fill((192,192,192), special_flags=pygame.BLEND_ADD)
        yield ghost, (x, y)

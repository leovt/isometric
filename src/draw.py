import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT

from world import load_assets, blits, View, update, Selector, Z_OFFSET, ElementType
import terrain

FPS = 60

assets = {}

def render_text(text, font, dst, pos):
    def blit_spec():
        x,y = pos
        for line in text.splitlines():
            surf = font.render(line.rstrip(), 1, pygame.Color("black"))
            yield surf, (x,y)
            y += surf.get_height()
    dst.blits(blit_sequence=blit_spec(), doreturn=False)


def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption(__file__)
    screen = pygame.display.set_mode((800,600), HWSURFACE|DOUBLEBUF|RESIZABLE)
    print(pygame.display.get_driver())
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    def show_info(selector):
        fps = str(int(clock.get_fps()))
        info = f'{fps} FPS\n{selector.details()}'
        render_text(info, font, screen, (10,10))

    load_assets()
    terrain.load_assets()

    running = True

    view = View(0, 400, 100, False)

    drag_start_coord = None
    drag_button = None

    do_update = True

    height_change_tile = None

    ghost = True

    while running:
        selector = Selector(pygame.mouse.get_pos())
        screen.fill((148, 179, 167))
        bls = list(blits(view, selector))
        screen.blits(blit_sequence=bls, doreturn=False)
        if ghost:
            screen.blits(blit_sequence=selector.ghost(), doreturn=False)
        show_info(selector)
        pygame.display.flip()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            view.x_offset -= 5
        if pressed[pygame.K_RIGHT]:
            view.x_offset += 5
        if pressed[pygame.K_UP]:
            view.y_offset -= 5
        if pressed[pygame.K_DOWN]:
            view.y_offset += 5



        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    w, h = screen.get_size()
                    view.rotate(w/2, h/2)
                if event.key==pygame.K_SPACE:
                    do_update = not do_update
                if event.key==pygame.K_4:
                    view.show_grid = not view.show_grid
            elif event.type==pygame.MOUSEBUTTONDOWN:
                drag_start_coord = event.pos
                drag_button = event.button
                if event.button == 1:
                    if selector.type == ElementType.TERRAIN_SURFACE:
                        height_change_tile = selector.element
                        height_change_tile.selected = True
                        height_change_tile.selected_corner = selector.subtile
                        ghost = False
                    else:
                        height_change_tile = None

            elif event.type==pygame.MOUSEBUTTONUP:
                drag_start_coord = None
                drag_button = None
                if height_change_tile:
                    height_change_tile.selected = False
                height_change_tile = None
                ghost = True

            elif event.type==pygame.MOUSEMOTION:
                if drag_button == 2:
                    view.x_offset += event.pos[0] - drag_start_coord[0]
                    view.y_offset += event.pos[1] - drag_start_coord[1]
                    drag_start_coord = event.pos
                elif drag_button == 1 and height_change_tile:
                    if event.pos[1] - drag_start_coord[1] > 2*Z_OFFSET:
                        height_change_tile.move_corner_down(height_change_tile.selected_corner)
                        drag_start_coord = drag_start_coord[0], drag_start_coord[1] + 2*Z_OFFSET
                    if event.pos[1] - drag_start_coord[1] < -2*Z_OFFSET:
                        height_change_tile.move_corner_up(height_change_tile.selected_corner)
                        drag_start_coord = drag_start_coord[0], drag_start_coord[1] - 2*Z_OFFSET


        dt = 0.001 * clock.tick(FPS)
        if do_update:
            update(dt)

if __name__ == '__main__':
    main()

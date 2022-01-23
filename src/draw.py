import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT

from world import load_assets, blits, View
FPS = 60

assets = {}

def main():
    pygame.init()
    pygame.display.set_caption(__file__)
    screen = pygame.display.set_mode((800,600), HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    def update_fps():
    	fps = str(int(clock.get_fps()))
    	fps_text = font.render(fps, 1, pygame.Color("black"))
    	return fps_text

    load_assets()

    running = True

    view = View(0, 400, 100)

    drag_start_coord = None

    while running:
        screen.fill((148, 179, 167))
        screen.blits(blit_sequence=blits(view, pygame.mouse.get_pos()), doreturn=False)
        screen.blit(update_fps(), (10,0))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            view.x_offset -= 5
        if pressed[pygame.K_RIGHT]:
            view.x_offset += 5
        if pressed[pygame.K_UP]:
            view.y_offset -= 5
        if pressed[pygame.K_DOWN]:
            view.y_offset += 5

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    w, h = screen.get_size()
                    view.rotate(w/2, h/2)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    drag_start_coord = event.pos
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    drag_start_coord = None
            elif event.type==pygame.MOUSEMOTION:
                if drag_start_coord:
                    view.x_offset += event.pos[0] - drag_start_coord[0]
                    view.y_offset += event.pos[1] - drag_start_coord[1]
                    drag_start_coord = event.pos

        clock.tick(FPS)

if __name__ == '__main__':
    main()

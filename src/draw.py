import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT

from world import load_assets, blits
FPS = 60

assets = {}

def main():
    pygame.init()
    pygame.display.set_caption(__file__)
    screen = pygame.display.set_mode((240,180), HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)


    def update_fps():
    	fps = str(int(clock.get_fps()))
    	fps_text = font.render(fps, 1, pygame.Color("black"))
    	return fps_text

    load_assets()

    running = True

    view_angle = 0

    while running:
        screen.fill((148, 179, 167))
        screen.blits(blit_sequence=blits(view_angle), doreturn=False)
        screen.blit(update_fps(), (10,0))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    view_angle = (view_angle + 1) % 4
        clock.tick(FPS*1000)

# def load_assets():
#     assets['ball'] = pygame.image.load('art/ball2.png').convert_alpha()
#
# balls = None
# def blits():
#     import random
#     global balls
#     if True or balls is None:
#         balls = [
#             (assets['ball'], (random.randrange(2000), random.randrange(1000)))
#             for _ in range(1000)
#         ]
#     return balls


if __name__ == '__main__':
    main()

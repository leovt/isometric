import pygame


class Grid:
    def __init__(self, parent, rows, cols, sticky):
        if isinstance(rows, int):
            self.rows = (1,) * rows
        else:
            self.rows = tuple(rows)

        if isinstance(cols, int):
            self.cols = (1,) * cols
        else:
            self.cols = tuple(cols)

        self.children = Grid._DummyDict()
        self.sticky = set(sticky.lower())
        assert self.sticky <= set('nwes')
        self.parent = parent
        self.width = 0
        self.height = 0

    class _DummyDict(dict):
        class Dummy:
            def min_width(self):
                return 0
            def min_height(self):
                return 0
        dummy = Dummy()
        def __missing__(self, key):
            return self.dummy

    def min_width(self):
        return sum(self.min_colwidths())

    def min_height(self):
        return sum(self.min_rowheights())

    def min_colwidths(self):
        print([(k,c.min_width()) for (k,c) in self.children.items()])
        return [max(self.children[i,j].min_width()
                       for i, w_row in enumerate(self.rows))
                   for j, w_col in enumerate(self.cols)]

    def min_rowheights(self):
        return [max(self.children[i,j].min_height()
                       for j, w_col in enumerate(self.cols))
                   for i, w_row in enumerate(self.rows)]

    def layout(self, width, height):
        tot_weigth = sum(self.cols)
        min_col = self.min_colwidths()
        delta = width - sum(min_col)
        if delta < 0:
            self.col_widths = min_col
            self.width = width
        elif 'w' in self.sticky and 'e' in self.sticky:
            self.col_widths = [m + delta/tot_weigth*w for (m,w) in zip(min_col, self.cols)]
            print(self.cols, min_col, delta, tot_weigth, self.col_widths)
            self.width = width
        else:
            self.col_widths = min_col
            self.width = sum(min_col)

        tot_weigth = sum(self.rows)
        min_row = self.min_rowheights()
        delta = height - sum(min_row)
        if delta < 0:
            self.row_heights = min_row
            self.height = height
        elif 's' in self.sticky and 'n' in self.sticky:
            self.row_heights = [m + delta/tot_weigth*w for (m,w) in zip(min_row, self.rows)]
            self.height = height
        else:
            self.row_heights = min_row
            self.height = sum(min_height)

        for (i,j), child in self.children.items():
            child.layout(self.col_widths[j], self.row_heights[i])


    def child_resize(self):
        if self.parent:
            self.parent.child_resize()
        else:
            self.layout(self.width, self.height)

    def draw(self, surf):
        for (i,j), child in self.children.items():
            left = sum(self.col_widths[:j])
            top = sum(self.row_heights[:i])
            width = child.min_width()
            height = child.min_height()

            if 'e' in child.sticky and 'w' in child.sticky:
                width = self.col_widths[j]
            elif 'e' in child.sticky:
                pass
            elif 'w' in child.sticky:
                left += self.col_widths[j] - width
            else:
                left += (self.col_widths[j] - width) // 2

            if 'n' in child.sticky and 's' in child.sticky:
                height = self.row_heights[i]
            elif 'n' in child.sticky:
                pass
            elif 's' in child.sticky:
                top += self.row_heights[i] - height
            else:
                top += (self.row_heights[i] - height) // 2

            rect = pygame.Rect(left, top, width, height)
            rect = rect.clip(surf.get_rect())
            if rect.width and rect.height:
                subsurf = surf.subsurface(rect)
                child.draw(subsurf)

class Button:
    def __init__(self, parent, text, font, sticky):
        self.text = text
        self.text_width, self.text_height = font.size(text)
        self.font = font
        self.sticky = set(sticky.lower())
        self.pressed = False
        assert self.sticky <= set('nwes')

    def min_width(self):
        return self.text_width + 10

    def min_height(self):
        return self.text_height + 10

    def layout(self, width, height):
        pass

    def draw(self, surf):
        w, h = surf.get_size()

        if self.pressed:
            surf.fill((0, 0, 0), (0,0,w-2,h-2))
            surf.fill((255, 255, 255), (2,2,w,h))
        else:
            surf.fill((0, 0, 0), (2,2,w,h))
            surf.fill((255, 255, 255), (0,0,w-2,h-2))
        surf.fill((194, 217, 178), (2,2,w-4,h-4))

        surf.blit(self.font.render(self.text, 1, pygame.Color("black")),
            ((w - self.text_width)//2, (h - self.text_height)//2))


class TopWindow(Grid):
    def __init__(self, text, font, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.text_width, self.text_height = font.size(text)
        self.font = font
        self.drag_pos = None

    def draw(self, surf):
        rect = pygame.Rect(self.left, self.top, self.width, self.height)
        rect = rect.clip(surf.get_rect())
        if rect.width and rect.height:
            sub = surf.subsurface(rect)
            sub.fill((128,112,144))
            sub.blit(self.font.render(self.text, 1, pygame.Color("black")),
            ((self.width - self.text_width - self.text_height)//2, 0))

    def on_mouse_down(self, event):
        self.drag_pos = event.pos

    def on_mouse_up(self, event):
        self.drag_pos = None

    def on_mouse_move(self, event):
        if self.drag_pos:
            print(self.drag_pos, event.pos)
            self.left += event.pos[0] - self.drag_pos[0]
            self.top += event.pos[1] - self.drag_pos[1]
            self.drag_pos = event.pos

import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT

def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption(__file__)
    screen = pygame.display.set_mode((800,600), HWSURFACE|DOUBLEBUF|RESIZABLE)
    font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    top = Grid(None, 3, 3, 'nwes')

    btn1 = Button(top, 'hello', font, 'nwes')
    btn2 = Button(top, 'hello, world!', font, 's')
    btn3 = Button(top, 'hi', font, 'ns')
    btn2.pressed = True

    tw = TopWindow('Window Title', font, 231, 111, 300, 200)

    top.children[2,0] = btn1
    top.children[2,1] = btn2
    top.children[1,2] = btn3
    top.layout(800, 600)

    running = True
    frame = 0
    while running:
        frame += 1
        screen.fill((148, 179, 167))
        top.draw(screen)
        tw.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                top.layout(*screen.get_size())
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
                if tw.left <= event.pos[0] < tw.left + tw.width and \
                   tw.top <= event.pos[1] < tw.top + tw.height:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        tw.on_mouse_down(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        tw.on_mouse_up(event)
                    elif event.type == pygame.MOUSEMOTION:
                        tw.on_mouse_move(event)

        clock.tick(30)

if __name__ == '__main__':
    main()

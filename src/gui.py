import pygame

class Widget:
    def __init__(self, parent):
        self.parent = parent
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.children = []
        if parent is not None:
            parent.register(self)

    def register(self, child):
        self.children.append(child)


from collections import namedtuple
ChildRef = namedtuple('ChildRef', 'row,col,widget,sticky')

class Frame(Widget):
    def __init__(self, parent, rows, cols, fixed_width=0, fixed_height=0, pad_left=0, pad_top=0, pad_right=0, pad_bottom=0):
        if isinstance(rows, int):
            self.row_weights = (1,) * rows
        else:
            self.row_weights = tuple(rows)

        if isinstance(cols, int):
            self.col_weights = (1,) * cols
        else:
            self.col_weights = tuple(cols)

        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

        self.rows = [list() for _ in self.row_weights]
        self.cols = [list() for _ in self.col_weights]
        self.managed_children = []

        Widget.__init__(self, parent)

    def manage_child_pos(self, row, col, widget, sticky=''):
        child = ChildRef(row, col, widget, sticky)
        self.rows[row].append(child)
        self.cols[col].append(child)
        self.managed_children.append(child)
        self.layout(self.width, self.height)

    def min_width(self):
        if self.fixed_width:
            return self.fixed_width
        return sum(self.min_colwidths())

    def min_height(self):
        if self.fixed_height:
            return self.fixed_height
        return sum(self.min_rowheights())

    def min_colwidths(self):
        return [max((x.widget.min_width() for x in row), default=0) for row in self.rows]

    def min_rowheights(self):
        return [max((x.widget.min_height() for x in col), default=0) for col in self.cols]

    def layout(self, width, height):
        if self.fixed_width:
            self.width = min(self.fixed_width, width)
        else:
            self.width = width

        tot_weight = sum(self.col_weights)
        min_col = self.min_colwidths()
        delta = self.width - sum(min_col)
        if delta < 0:
            self.col_widths = min_col
        else:
            self.col_widths = [m + delta/tot_weight*w for (m,w) in zip(min_col, self.col_weights)]

        if self.fixed_height:
            self.height = min(self.fixed_height, height)
        else:
            self.height = height
        tot_weight = sum(self.row_weights)
        min_row = self.min_rowheights()
        delta = self.height - sum(min_row)
        if delta < 0:
            self.row_heights = min_row
        else:
            self.row_heights = [m + delta/tot_weight*w for (m,w) in zip(min_row, self.row_weights)]

        for child in self.managed_children:
            i, j = child.row, child.col
            left = sum(self.col_widths[:j])
            top = sum(self.row_heights[:i])
            width = child.widget.min_width()
            height = child.widget.min_height()

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

            child.widget.left = left
            child.widget.top = top
            child.widget.width = width
            child.widget.height = height
            try:
                child.widget.layout(self.col_widths[child.col], self.row_heights[child.row])
            except AttributeError:
                pass

    def draw(self, surf, offset_x, offset_y):
        for child in self.children:
            rect = pygame.Rect(child.left - offset_x, child.top - offset_y, child.width, child.height)
            rect = rect.clip(surf.get_rect())
            if rect.width and rect.height:
                subsurf = surf.subsurface(rect)
                child.draw(subsurf, rect.left-child.left, rect.top-child.top)

class Button(Widget):
    def __init__(self, parent, text, font):
        Widget.__init__(self, parent)
        self.text = text
        self.text_width, self.text_height = font.size(text)
        self.font = font
        self.pressed = False

    def min_width(self):
        return self.text_width + 10

    def min_height(self):
        return self.text_height + 10

    def layout(self, width, height):
        pass

    def draw(self, surf, offset_x, offset_y):
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


class TopWindow(Frame):
    def __init__(self, parent, text, font, cols, rows, left, top, width, height):
        self.text_width, self.text_height = font.size(text)
        Frame.__init__(self, parent, cols, rows, pad_top = self.text_height)
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.drag_pos = None

    def draw(self, surf, offset_x, offset_y):
        surf.fill((128,112,144))
        surf.blit(self.font.render(self.text, 1, pygame.Color("black")),
            ((self.width - self.text_width - self.text_height)//2 - offset_x, -offset_y))
        Frame.draw(self, surf, offset_x, offset_y)

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

    root = Frame(None, 3, 3)

    btn1 = Button(root, 'hello', font)
    btn2 = Button(root, 'hello, world!', font)
    btn3 = Button(root, 'hi', font)
    btn2.pressed = True

    root.manage_child_pos(2, 0, btn1, 'nwes')
    root.manage_child_pos(2, 1, btn2, 's')
    root.manage_child_pos(1, 2, btn3, 'ns')

    tw = TopWindow(root, 'Window Title', font, 1, 1, 231, 111, 300, 200)

    btn4 = Button(tw, 'Button 4', font)
    tw.manage_child_pos(0,0,btn4,'')

    assert tw in root.children
    root.layout(800, 600)

    running = True
    frame = 0
    while running:
        frame += 1
        screen.fill((148, 179, 167))
        root.draw(screen, 0, 0)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                root.layout(*screen.get_size())
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

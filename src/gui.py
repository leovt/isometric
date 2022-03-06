import pygame
import ctypes
import ctypes.wintypes

class Widget:
    def __init__(self, parent):
        self.parent = parent
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.children = []
        self.border = None
        self.background = None
        self.relief = 'flat'

        if parent is not None:
            parent.register(self)

    def register(self, child):
        self.children.append(child)

    def draw(self, surf, offset_x, offset_y):
        if self.background is not None:
            surf.fill(self.background)

        highlight = (255, 255, 255)
        shadow = (0, 0, 0)

        if self.border is not None:
            if self.relief == 'raised':
                tl = highlight
                br = shadow
            elif self.relief == 'sunken':
                tl = shadow
                br = highlight

            if self.relief in ('raised, sunken'):
                a,b,c,d = -offset_x, self.border - offset_x, self.width - self.border - offset_x, self.width - offset_x
                u,v,w,x = -offset_y, self.border - offset_y, self.height - self.border - offset_y, self.height - offset_y
                pygame.draw.polygon(surf, tl, [
                    (a,u),
                    (d,u),
                    (c,v),
                    (b,v),
                    (b,w),
                    (a,x),
                    (a,u),])
                pygame.draw.polygon(surf, br, [
                    (d,x),
                    (a,x),
                    (b,w),
                    (c,w),
                    (c,v),
                    (d,u),
                    (d,x),])

        if hasattr(self, 'client_draw'):
            self.client_draw(surf, offset_x, offset_y)
        for child in self.children:
            rect = pygame.Rect(child.left - offset_x, child.top - offset_y, child.width, child.height)
            rect = rect.clip(surf.get_rect())
            if rect.width and rect.height:
                subsurf = surf.subsurface(rect)
                child.draw(subsurf, rect.left-child.left, rect.top-child.top)


from collections import namedtuple
ChildRef = namedtuple('ChildRef', 'row,col,widget,sticky')

class MouseEventMixin:
    mouse_focus_child = None
    def process_mouse_event(self, event, local_pos = None):
        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            return
        if local_pos is None:
            local_pos = event.pos

        if self.mouse_focus_child is None:
            for child in self.children:
                if (hasattr(child, 'process_mouse_event') and
                    child.left <= local_pos[0] < child.left + child.width and
                    child.top <= local_pos[1] < child.top + child.height):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_focus_child = child

        if self.mouse_focus_child is not None:
            self.mouse_focus_child.process_mouse_event(event, (local_pos[0] - self.mouse_focus_child.left, local_pos[1] - self.mouse_focus_child.top))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'on_mouse_down'):
                self.on_mouse_down(event)
            elif event.type == pygame.MOUSEMOTION and hasattr(self, 'on_mouse_move'):
                self.on_mouse_move(event)
            elif event.type == pygame.MOUSEBUTTONUP and hasattr(self, 'on_mouse_up'):
                self.on_mouse_up(event)

        if event.type == pygame.MOUSEBUTTONUP and self.mouse_focus_child is not None:
            del self.mouse_focus_child



class Frame(Widget, MouseEventMixin):
    def __init__(self, parent, rows, cols, fixed_width=0, fixed_height=0, pad_left=0, pad_top=0, pad_right=0, pad_bottom=0):
        self.pad_left = pad_left
        self.pad_top = pad_top
        self.pad_right = pad_right
        self.pad_bottom = pad_bottom

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
        return sum(self.min_colwidths()) + self.pad_left + self.pad_right

    def min_height(self):
        if self.fixed_height:
            return self.fixed_height
        return sum(self.min_rowheights()) + self.pad_top + self.pad_bottom

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
            left = sum(self.col_widths[:j]) + self.pad_left
            top = sum(self.row_heights[:i]) + self.pad_top
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

class Button(Widget, MouseEventMixin):
    def __init__(self, parent, text, font):
        Widget.__init__(self, parent)
        self.text = text
        self.text_width, self.text_height = font.size(text)
        self.font = font
        self.command = int
        self.background = (194, 217, 178)
        self.border = 4
        self.relief = 'raised'

    def min_width(self):
        return self.text_width + size(10) + 2*self.border

    def min_height(self):
        return self.text_height + size(10) + 2*self.border

    def layout(self, width, height):
        pass

    def client_draw(self, surf, offset_x, offset_y):
        w, h = surf.get_size()
        surf.blit(self.font.render(self.text, 1, pygame.Color("black")),
            ((w - self.text_width)//2, (h - self.text_height)//2))

    def on_mouse_down(self, event):
        self.relief = 'sunken'

    def on_mouse_up(self, event):
        self.relief = 'raised'
        self.command()


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
        self.border = size(1)
        self.background = (123, 45, 67)
        self.relief = 'raised'

    def client_draw(self, surf, offset_x, offset_y):
        surf.blit(self.font.render(self.text, 1, pygame.Color("black")),
            ((self.width - self.text_width - self.text_height)//2 - offset_x, -offset_y))

    def on_mouse_down(self, event):
        self.drag_pos = event.pos

    def on_mouse_up(self, event):
        self.drag_pos = None

    def on_mouse_move(self, event):
        if self.drag_pos:
            self.left += event.pos[0] - self.drag_pos[0]
            self.top += event.pos[1] - self.drag_pos[1]
            self.drag_pos = event.pos

dpi = 96
def make_dpi_aware():
    global dpi
    DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = ctypes.wintypes.HANDLE(-2)
    ctypes.windll.user32.SetThreadDpiAwarenessContext(DPI_AWARENESS_CONTEXT_SYSTEM_AWARE)
    dpi = ctypes.windll.user32.GetDpiForSystem()

def size(base):
    return base * dpi // 96

import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT

def main():
    make_dpi_aware()
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption(__file__)
    screen = pygame.display.set_mode((size(800), size(600)), HWSURFACE|DOUBLEBUF|RESIZABLE)
    font_size = size(18)
    font = pygame.font.SysFont("Arial", font_size)
    clock = pygame.time.Clock()

    root = Frame(None, 3, 3)

    btn1 = Button(root, 'hello', font)
    btn2 = Button(root, 'hello, world!', font)
    btn3 = Button(root, 'hi', font)

    root.manage_child_pos(2, 0, btn1, 'nwes')
    root.manage_child_pos(2, 1, btn2, 's')
    root.manage_child_pos(1, 2, btn3, 'ns')

    tw = TopWindow(root, 'Window Title', font, 1, 1, size(231), size(111), size(300), size(200))

    btn4 = Button(tw, 'Button 4', font)
    btn4.border = size(10)
    tw.manage_child_pos(0,0,btn4,'n')

    assert tw in root.children
    root.layout(*screen.get_size())

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
                root.process_mouse_event(event)

        clock.tick(30)

if __name__ == '__main__':
    main()

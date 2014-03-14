__version__ = '1.0.1'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, BorderImage
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from random import choice


class Number(Widget):
    number = NumericProperty(2)
    scale = NumericProperty(.1)
    colors = {
        2: get_color_from_hex('#eee4da'),
        4: get_color_from_hex('#ede0c8'),
        8: get_color_from_hex('#f2b179'),
        16: get_color_from_hex('#f59563'),
        32: get_color_from_hex('#f67c5f'),
        64: get_color_from_hex('#f65e3b'),
        128: get_color_from_hex('#edcf72'),
        256: get_color_from_hex('#edcc61'),
        512: get_color_from_hex('#edc850'),
        1024: get_color_from_hex('#edc53f'),
        2048: get_color_from_hex('#edc22e')}

    def __init__(self, **kwargs):
        super(Number, self).__init__(**kwargs)
        anim = Animation(scale=1., d=.15, t='out_quad')
        anim.bind(on_complete=self.clean_canvas)
        anim.start(self)

    def clean_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

    def move_to_and_destroy(self, pos):
        self.destroy()
        #anim = Animation(opacity=0., d=.25, t='out_quad')
        #anim.bind(on_complete=self.destroy)
        #anim.start(self)

    def destroy(self, *args):
        self.parent.remove_widget(self)

    def move_to(self, pos):
        if self.pos == pos:
            return
        Animation(pos=pos, d=.1, t='out_quad').start(self)


class Game2048(Widget):

    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Game2048, self).__init__()
        self.grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]

        # bind keyboard
        Window.bind(on_key_down=self.on_key_down)

        self.restart()

    def on_key_down(self, window, key, *args):
        if key == 273:
            self.move_topdown(True)
        elif key == 274:
            self.move_topdown(False)
        elif key == 276:
            self.move_leftright(False)
        elif key == 275:
            self.move_leftright(True)

    def rebuild_background(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0xbb / 255., 0xad / 255., 0xa0 / 255.)
            BorderImage(pos=self.pos, size=self.size, source='data/round.png')
            Color(0xcc / 255., 0xc0 / 255., 0xb3 / 255.)
            csize = self.cube_size, self.cube_size
            for ix, iy in self.iterate_pos():
                BorderImage(pos=self.index_to_pos(ix, iy), size=csize,
                source='data/round.png')


    def reposition(self, *args):
        self.rebuild_background()
        # calculate the size of a number
        l = min(self.width, self.height)
        padding = (l / 4.) / 8.
        cube_size = (l - (padding * 5)) / 4.
        self.cube_size = cube_size
        self.cube_padding = padding

        for ix, iy, number in self.iterate():
            number.size = cube_size, cube_size
            number.pos = self.index_to_pos(ix, iy)

    def iterate(self):
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_empty(self):
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if not child:
                yield ix, iy

    def iterate_pos(self):
        for ix in range(4):
            for iy in range(4):
                yield ix, iy

    def index_to_pos(self, ix, iy):
        padding = self.cube_padding
        cube_size = self.cube_size
        return [
            (self.x + padding) + ix * (cube_size + padding),
            (self.y + padding) + iy * (cube_size + padding)]

    def spawn_number(self, *args):
        empty = list(self.iterate_empty())
        if not empty:
            return
        ix, iy = choice(empty)
        number = Number(
                size=(self.cube_size, self.cube_size),
                pos=self.index_to_pos(ix, iy))
        self.grid[ix][iy] = number
        self.add_widget(number)

    def on_touch_up(self, touch):
        v = Vector(touch.pos) - Vector(touch.opos)
        if v.length() < dp(20):
            return

        # detect direction
        dx, dy = v
        if abs(dx) > abs(dy):
            self.move_leftright(dx > 0)
        else:
            self.move_topdown(dy > 0)

    def move_leftright(self, right):
        r = range(3, -1, -1) if right else range(4)
        grid = self.grid
        moved = False

        for iy in range(4):
            # get all the cube for the current line
            cubes = []
            for ix in r:
                cube = grid[ix][iy]
                if cube:
                    cubes.append(cube)

            # combine them
            self.combine(cubes)

            # update the grid
            for ix in r:
                cube = cubes.pop(0) if cubes else None
                if grid[ix][iy] != cube:
                    moved = True
                grid[ix][iy] = cube
                if not cube:
                    continue
                pos = self.index_to_pos(ix, iy)
                if cube.pos != pos:
                    cube.move_to(pos)

        if not self.check_end() and moved:
            Clock.schedule_once(self.spawn_number, .20)

    def move_topdown(self, top):
        r = range(3, -1, -1) if top else range(4)
        grid = self.grid
        moved = False

        for ix in range(4):
            # get all the cube for the current line
            cubes = []
            for iy in r:
                cube = grid[ix][iy]
                if cube:
                    cubes.append(cube)

            # combine them
            self.combine(cubes)

            # update the grid
            for iy in r:
                cube = cubes.pop(0) if cubes else None
                if grid[ix][iy] != cube:
                    moved = True
                grid[ix][iy] = cube
                if not cube:
                    continue
                pos = self.index_to_pos(ix, iy)
                if cube.pos != pos:
                    cube.move_to(pos)

        if not self.check_end() and moved:
            Clock.schedule_once(self.spawn_number, .20)

    def combine(self, cubes):
        if len(cubes) <= 1:
            return cubes
        index = 0
        while index < len(cubes) - 1:
            cube1 = cubes[index]
            cube2 = cubes[index + 1]
            if cube1.number == cube2.number:
                cube1.number *= 2
                self.score += cube1.number
                cube2.move_to_and_destroy(cube1.pos)
                del cubes[index + 1]
                index += 1

            index += 1

    def check_end(self):
        # we still have empty space
        if any(self.iterate_empty()):
            return False

        # check if 2 numbers of the same type are near each others
        if self.have_available_moves():
            return False

        self.end()
        return True

    def have_available_moves(self):
        grid = self.grid
        for iy in range(4):
            for ix in range(3):
                cube1 = grid[ix][iy]
                cube2 = grid[ix + 1][iy]
                if cube1.number == cube2.number:
                    return True

        for ix in range(4):
            for iy in range(3):
                cube1 = grid[ix][iy]
                cube2 = grid[ix][iy + 1]
                if cube1.number == cube2.number:
                    return True

    def end(self):
        end = self.ids.end
        self.remove_widget(end)
        self.add_widget(end)
        text = 'Game\nover!'
        for ix, iy, cube in self.iterate():
            if cube.number == 2048:
                text = 'WIN !'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)

    def restart(self):
        self.score = 0
        for ix, iy, child in self.iterate():
            child.destroy()
        self.grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]
        self.reposition()
        Clock.schedule_once(self.spawn_number, .1)
        self.ids.end.opacity = 0


class Game2048App(App):
    def on_pause(self):
        return True

if __name__ == '__main__':
    Game2048App().run()

PyGameUX BETA V0.1
===============
Versão __Beta__ de um projeto que, usando pygame com SDL2, poderá
desde fazer interfaces quanto jogos com um código organizado e
orientado a objetos.

Instalando
============
    pip install pygameux

Como Usar
=====
#### main.py
```
from mainscene import MainScene
from pygameui import Core

program_ui = Core()
program_ui.window.set_size(720, 405)
program_ui.looptimer.set_fps(60)
program_ui.scenes.set_current_scene(MainScene(program_ui))
program_ui.run()
```
#### mainscene.py
```py
from pygameui import Scene
from testnode import TestNode


class MainScene(Scene):
    def __init__(self, program):
        super().__init__(program)

    def process(self):
        super().process()
        
        self.add_child(TestNode(self))
        
        # exit
        if self.program.events.system.get_exit_requested():
            self.program.exit()
```
#### testnode.py
```py
from random import randint

import pygame

from pygameui import ColorRect


class TestNode(ColorRect):
    def __init__(self, parent):
        w, h = 50, 50
        x = randint(0, parent.program.window.size.width - w)
        y = randint(0, parent.program.window.size.height - h)

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        super().__init__(parent, (r, g, b), pygame.Rect(x, y, w, h))
```
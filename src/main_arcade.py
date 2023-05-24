import arcade

from settings import *

class Main(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH_SIZE, HEIGHT_SIZE, title="LifeBox Simulator", resizable=True, center_window=True)

        arcade.set_background_color((21, 36, 36))

    def on_draw(self):
        self.clear()

def run_simulation():
    window = Main()
    arcade.run()


if __name__ == "__main__":
    run_simulation()
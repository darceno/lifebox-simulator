import arcade

from settings import *

class Organism(arcade.SpriteCircle):
    def __init__(self, x, y, size, color, genome):
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        self.genome = genome
        self.possible_genes = ["CR", "RA", "MM"]

class Simulation(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)

        arcade.set_background_color((21, 36, 36))

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

def main():
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()


if __name__ == "__main__":
    main()
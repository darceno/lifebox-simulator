import arcade
import random

from settings import *

class Organism(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.genome = []
        self.possible_genes = ["CR", "RA", "MM"]

class Simulation(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)
        self.organisms = None

        arcade.set_background_color((21, 36, 36))

    def setup(self):
        self.organisms = arcade.SpriteList()
        self.create_organisms()

    def on_draw(self):
        self.clear()
        self.organisms.draw()

    def on_update(self, delta_time):
        pass

    def create_organisms(self):
        for i in range(STARTING_POPULATION):
            organism = Organism("assets/organism_sprite.png", 1)
            organism.center_x = random.randrange(64, WIDTH_SIZE-64)
            organism.center_y = random.randrange(64, HEIGHT_SIZE-64)
            self.organisms.append(organism)

def main():
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade
import random
import time

from settings import *

class Organism(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.genome = []
        self.possible_genes = ["CR", "RA", "MM"]
        self.decision_delay = 0.08
        self.speed = 1

    def move_decision(self):
        if random.random() < self.decision_delay:
            self.change_x = random.uniform(-self.speed, self.speed)
            self.change_y = random.uniform(-self.speed, self.speed)

        if self.center_x < ORGANISM_RADIUS or self.center_x > WIDTH_SIZE - ORGANISM_RADIUS:
            self.change_x *= -1
        if self.center_y < ORGANISM_RADIUS or self.center_y > HEIGHT_SIZE - ORGANISM_RADIUS:
            self.change_y *= -1

    def move(self):
        self.move_decision()

        self.center_x += self.change_x
        self.center_y += self.change_y

    def update(self):
        self.universal_abilities()
        self.genetic_abilities()

    def universal_abilities(self):
        pass

    def genetic_abilities(self):
        if "MM" in self.genome:
            self.move() 

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
        self.organisms.update()

    def create_organisms(self):
        for i in range(STARTING_POPULATION):
            organism = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
            organism.center_x = random.randrange(64, WIDTH_SIZE-64)
            organism.center_y = random.randrange(64, HEIGHT_SIZE-64)
            self.organisms.append(organism)

def main():
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()


if __name__ == "__main__":
    main()
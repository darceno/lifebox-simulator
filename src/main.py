import arcade
import random
import time

from settings import *

class Organism(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.genome = ["CRc", "RA"]
        self.possible_genes = ["CRa", "CRb", "CRc", "RA", "MM"]
        self.decision_delay = 0.08
        self.speed = 42
        self.energy = 5
        self.last_consumption = time.time()
        self.last_CR = 0
        self.alive = True

    def update(self):
        self.universal_abilities()
        self.genetic_abilities()

    def universal_abilities(self):
        self.energy_consumption()
        self.death()

    def genetic_abilities(self):
        cellular_respiration_genes = ["CRa", "CRb", "CRc"]
        if any(gene in cellular_respiration_genes for gene in self.genome):
            self.cellular_respiration()
        if "MM" in self.genome:
            self.move() 

    def energy_consumption(self):
        if time.time() - self.last_consumption > 1:
            self.energy -= len(self.genome) + self.speed
            self.last_consumption = time.time()

    def death(self):
        if self.energy <= 0:
            self.alive = False
        if len(self.genome) == 0:
            self.alive = False

    def cellular_respiration(self):
        if self.last_CR == 0:
            self.last_CR = time.time()
        if time.time() - self.last_CR > 1:
            if "CRa" in self.genome:
                self.energy += 8
            elif "CRb" in self.genome:
                self.energy += 6
            elif "CRc" in self.genome:
                self.energy += 4
            self.last_CR = time.time()

    def move(self):
        self.move_decision()

        self.center_x += self.change_x * dt
        self.center_y += self.change_y * dt

    def move_decision(self):
        if random.random() < self.decision_delay:
            self.change_x = random.uniform(-self.speed, self.speed)
            self.change_y = random.uniform(-self.speed, self.speed)

        if self.center_x < ORGANISM_RADIUS or self.center_x > WIDTH_SIZE - ORGANISM_RADIUS:
            self.change_x *= -1
        if self.center_y < ORGANISM_RADIUS or self.center_y > HEIGHT_SIZE - ORGANISM_RADIUS:
            self.change_y *= -1

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
        global dt
        dt = delta_time
        self.organisms.update()
        self.check_if_dead()

    def create_organisms(self):
        for i in range(STARTING_POPULATION):
            organism = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
            organism.center_x = random.randrange(64, WIDTH_SIZE-64)
            organism.center_y = random.randrange(64, HEIGHT_SIZE-64)
            self.organisms.append(organism)

    def check_if_dead(self):
        for organism in self.organisms:
            if organism.alive == False:
                organism.remove_from_sprite_lists()

def main():
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade
import random
import time

from settings import *

class Organism(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.genome = []
        self.possible_genes = ["CR", "RA", "MM"]
        self.last_decision = 0

    def move_decision(self):
        self.decision = random.randint(0, 7) # 0/right - 1/left - 1/down - 3/up - 4/right-down - 5/right-up - 6/left-down - 7/left-up
        decision_options = [1, 1, 1, 1, 1, 1, 1, 3, 3, 4]
        self.decision_delay = random.choice(decision_options)
        self.last_decision = time.time()

    def move(self):
        if self.last_decision == 0:
            self.move_decision()
        if time.time() - self.last_decision > self.decision_delay:
            self.move_decision()

        self.change_x = 0
        self.change_y = 0
        
        if self.decision == 0 and self.right + SPEED < WIDTH_SIZE: #right
            self.change_x += SPEED
        elif self.decision == 1 and self.left - SPEED > 0: #left
            self.change_x -= SPEED
        elif self.decision == 1 and self.bottom - SPEED < 0: #down
            self.change_y -= SPEED
        elif self.decision == 3 and self.top + SPEED < HEIGHT_SIZE: #up
            self.change_y += SPEED
        elif self.decision == 4 and self.right + SPEED < WIDTH_SIZE and self.bottom - 1 > 0: #right-down
            self.change_x += SPEED
            self.change_y -= SPEED
        elif self.decision == 5 and self.right + SPEED < WIDTH_SIZE and self.top + SPEED < HEIGHT_SIZE: #right-up
            self.change_x += SPEED
            self.change_y += SPEED
        elif self.decision == 6 and self.left - SPEED > 0 and self.bottom - SPEED > 0: #left-down
            self.change_x -= SPEED
            self.change_y -= SPEED
        elif self.decision == 7 and self.left - SPEED > 0 and self.top + SPEED < HEIGHT_SIZE: #left-up
            self.change_x -= SPEED
            self.change_y += SPEED
        else:
            self.move_decision()

        self.center_x += self.change_x
        self.center_y += self.change_y

    def update(self):
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
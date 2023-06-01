import arcade
import random
import time

from settings import *
from gene_colors import gene_colors

class Organism(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.genome = ["CRc", "RA"]
        self.possible_genes = ["CRa", "CRb", "CRc", "RA", "MM"]
        self.decision_delay = 0.08
        self.speed = 42
        self.energy = 5
        self.age = 0
        self.last_birthday = time.time()
        self.last_consumption = time.time()
        self.last_CR = 0
        self.alive = True
        self.min_reserved_energy = 5

    def update(self):
        self.universal_abilities()
        self.genetic_abilities()

    def universal_abilities(self):
        self.energy_consumption()
        self.death()
        self.color_change()

    def genetic_abilities(self):
        cellular_respiration_genes = ["CRa", "CRb", "CRc"]
        if any(gene in cellular_respiration_genes for gene in self.genome):
            self.cellular_respiration()
        if "RA" in self.genome:
            self.asexual_reproduction()
        if "MM" in self.genome:
            self.move() 

    def energy_consumption(self):
        if time.time() - self.last_consumption > 1:
            self.energy -= len(self.genome)
            self.last_consumption = time.time()

    def aging(self):
        if time.time() - self.last_birthday > YEAR:
            self.age += 1
            self.last_birthday = time.time()

    def death(self):
        if self.energy <= 0:
            self.alive = False
        if self.age >= len(self.genome):
            self.alive = False
        if len(self.genome) == 0:
            self.alive = False

    def color_change(self):
        red_component = []
        green_component = []
        blue_component = []

        for gene in self.genome:
            if gene in gene_colors:
                color = gene_colors[gene]
                red_component.append(color[0])
                green_component.append(color[1])
                blue_component.append(color[2])

        if not red_component:
            red_component = [255]
        if not green_component:
            green_component = [255]
        if not blue_component:
            blue_component = [255]

        red_value = sum(red_component) / len(red_component)
        green_value = sum(green_component) / len(green_component)
        blue_value = sum(blue_component) / len(blue_component)

        self.color = (red_value, green_value, blue_value)

    def cellular_respiration(self):
        if self.last_CR == 0:
            self.last_CR = time.time()
        if time.time() - self.last_CR > 1:
            if "CRa" in self.genome:
                self.energy += 10
            elif "CRb" in self.genome:
                self.energy += 7
            elif "CRc" in self.genome:
                self.energy += 5
            self.last_CR = time.time()

    def asexual_reproduction(self):
        if self.energy > COST_TO_REPRODUCE + (len(self.genome)*2) + self.min_reserved_energy:
            if random.random() <= REPRODUCTION_SUCESS_RATE:
                offspring = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
                offspring.center_x = self.center_x 
                offspring.center_y = self.center_y
                offspring.birth_location()
                offspring.mutation()
                simulation.spawn_offspring(offspring)
                self.energy -= COST_TO_REPRODUCE + (len(self.genome)*2)
            else:
                self.energy -= COST_TO_REPRODUCE

    def birth_location(self):
        self.center_x = random.choice([self.center_x, self.center_x - ORGANISM_RADIUS, self.center_x + ORGANISM_RADIUS])
        self.center_y = random.choice([self.center_y, self.center_y - ORGANISM_RADIUS, self.center_y + ORGANISM_RADIUS])

    def mutation(self):
        if random.random() <= MUTATION_CHANCE:
            mutation_type = random.randint(1, 3)
            if mutation_type == 1:
                new_gene = random.choice(self.possible_genes)
                self.genome.append(new_gene)
            elif mutation_type == 2:
                new_gene = random.choice(self.possible_genes)
                ex_gene = random.choice(self.genome)
                self.genome.append(new_gene)
                self.genome.remove(ex_gene)
            elif mutation_type == 3:
                ex_gene = random.choice(self.genome)
                self.genome.remove(ex_gene)

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

    def on_mouse_press(self, x, y: int, button, modifiers):
        for organism in self.organisms:
            if organism.collides_with_point((x, y)):
                print(sorted(organism.genome))

    def create_organisms(self):
        for i in range(STARTING_POPULATION):
            organism = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
            organism.center_x = random.randrange(64, WIDTH_SIZE-64)
            organism.center_y = random.randrange(64, HEIGHT_SIZE-64)
            if START_WITH_MUTATION:
                organism.mutation()
            self.organisms.append(organism)

    def spawn_offspring(self, offspring):
        self.organisms.append(offspring)

    def check_if_dead(self):
        for organism in self.organisms:
            if organism.alive == False:
                organism.remove_from_sprite_lists()

def main():
    global simulation
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()


if __name__ == "__main__":
    main()
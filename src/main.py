import arcade
import random
import time

import event_logging
from ecosystem import *
from settings import *
from gene_colors import gene_colors

class Organism(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.name = None
        self.genome = ["CRc", "RA", "MM"]
        self.possible_genes = ["CRa", "CRb", "CRc", "RA", "MM", "SPa", "SPb", "DDa", "DDb"]
        self.alive = True
        self.age = 0
        self.speed = 42
        self.decision_delay = 0.08
        self.min_reserved_energy = 5
        self.energy = 5
        self.last_birthday = time.time()
        self.last_consumption = time.time()
        self.last_CR = 0

    def print_info(self):
        print("-----------------------")
        print(f"Name: {self.name}" +
            f"\nGenome: " + ", ".join(sorted(self.genome)) +
            f"\nAge: {self.age} years" +
            f"\nEnergy: {self.energy} points" +
            f"\nSpeed: {self.speed}" +
            f"\nDecision delay: {self.decision_delay}")
        print("-----------------------")

    def update(self):
        self.universal_abilities()
        self.genetic_abilities()
        self.genetic_attributes()

    def universal_abilities(self):
        self.energy_consumption()
        self.death()
        self.color_change()
        self.aging()

    def genetic_abilities(self):
        cellular_respiration_genes = ["CRa", "CRb", "CRc"]
        if any(gene in cellular_respiration_genes for gene in self.genome):
            self.cellular_respiration()

        if "RA" in self.genome:
            self.asexual_reproduction()
        if "MM" in self.genome:
            self.move() 

    def genetic_attributes(self):
        if "SPa" in self.genome:
            self.speed = 42 + (self.genome.count("SPa") * 20)
            if self.speed > 102: self.speed = 102
        if "SPb" in self.genome:
            self.speed = 42 - (self.genome.count("SPb") * 20)
            if self.speed < 2: self.speed = 2

        if "DDa" in self.genome:
            self.decision_delay = 0.08 - (self.genome.count("DDa") * 0.02)
            if self.decision_delay < 0.01: self.decision_delay = 0.01
        if "DDb" in self.genome:
            self.decision_delay = 0.08 + (self.genome.count("DDb") * 0.02)
            if self.decision_delay > 0.2: self.decision_delay = 0.2

    def energy_consumption(self):
        if time.time() - self.last_consumption > 1 / simulation_speed:
            self.energy -= len(self.genome)
            self.last_consumption = time.time()

    def aging(self):
        if time.time() - self.last_birthday > YEAR / simulation_speed:
            self.age += 1
            self.last_birthday = time.time()
            event_logging.birthday(self.name, self.age)

    def death(self):
        if self.energy <= 0:
            self.alive = False
            event_logging.death_energy(self.name)
            
        if self.age >= len(self.genome):
            self.alive = False
            event_logging.death_age(self.name, self.age)

        if len(self.genome) == 0:
            self.alive = False
            event_logging.death_gene_depletion(self.name)

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
        if time.time() - self.last_CR > 1 / simulation_speed:
            if "CRa" in self.genome and eco.energy_avaliable > 8:
                self.energy += 8
                eco.energy_avaliable -= 8
            elif "CRb" in self.genome and eco.energy_avaliable > 6:
                self.energy += 6
                eco.energy_avaliable -= 6
            elif "CRc" in self.genome and eco.energy_avaliable > 4:
                self.energy += 4
                eco.energy_avaliable -= 4
            self.last_CR = time.time()

    def asexual_reproduction(self):
        global organism_name

        if self.energy > COST_TO_REPRODUCE + (len(self.genome)*2) + self.min_reserved_energy:
            if random.random() <= REPRODUCTION_SUCESS_RATE:
                offspring = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
                offspring.center_x = self.center_x 
                offspring.center_y = self.center_y
                offspring.genome = self.genome[:]
                offspring.name = organism_name

                event_logging.asexual_reproduction(self.name, offspring.name) # event log
                
                offspring.birth_location()
                offspring.mutation()
                simulation.spawn_offspring(offspring)
                organism_name += 1
                self.energy -= COST_TO_REPRODUCE + (len(self.genome)*2)


            else:
                self.energy -= COST_TO_REPRODUCE

    def birth_location(self):
        self.center_x = random.choice([self.center_x, self.center_x - ORGANISM_RADIUS, self.center_x + ORGANISM_RADIUS])
        self.center_y = random.choice([self.center_y, self.center_y - ORGANISM_RADIUS, self.center_y + ORGANISM_RADIUS])

    def mutation(self):
        if random.random() <= MUTATION_CHANCE:
            mutation_type = random.randint(1, 3)
            if mutation_type == 1: # addition of a gene
                new_gene = random.choice(self.possible_genes)
                self.genome.append(new_gene)
            elif mutation_type == 2: # subtraction of a gene
                ex_gene = random.choice(self.genome)
                self.genome.remove(ex_gene)
            elif mutation_type == 3: # replacement of a gene
                new_gene = random.choice(self.possible_genes)
                ex_gene = random.choice(self.genome)
                self.genome.append(new_gene)
                self.genome.remove(ex_gene)

            event_logging.mutation_occurred(self.name) # event log

        else:
            event_logging.mutation_not_occurred(self.name) # event log

    def move(self):
        self.move_decision()
        self.center_x += self.change_x * dt * simulation_speed
        self.center_y += self.change_y * dt * simulation_speed

    def move_decision(self):
        if random.random() < self.decision_delay * simulation_speed:
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
        self.start_time = time.time()

        arcade.set_background_color(BG_COLOR)

        self.show_panel = False

    def setup(self):
        global eco
        self.organisms = arcade.SpriteList()
        self.create_organisms()
        eco = Ecosystem()

    def on_draw(self):
        self.clear()
        self.organisms.draw()

        if self.show_panel:
            self.time_line.draw()
            self.speed_line.draw()
            self.energy_line.draw()
            self.population_line.draw()

    def on_update(self, delta_time):
        global dt
        global eco
        dt = delta_time
        self.simulation_time = time.time() - self.start_time
        self.organisms.update()
        self.check_if_dead()
        eco.energy_updade()
        self.information_panel()

    def information_panel(self):
        last_line_Y = 20
        start_x = 10
        start_y = last_line_Y

        time_info = (f"Simulation time: {round(self.simulation_time)} seconds")
        self.time_line = arcade.Text(time_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE )

        start_y = last_line_Y + LINE_HEIGHT
        speed_info = (f"Simulation speed: {simulation_speed}x")
        self.speed_line = arcade.Text(speed_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)

        start_y = last_line_Y + LINE_HEIGHT * 2
        energy_info = (f"Energy avaliable: {eco.energy_avaliable}")
        self.energy_line = arcade.Text(energy_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)
        
        start_y = last_line_Y + LINE_HEIGHT * 3
        population_info = (f"Population: {len(self.organisms)}")
        self.population_line = arcade.Text(population_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)

    def print_info_simulation(self):
        print("-----------------------")
        print(f"Population: {len(self.organisms)}" +
            f"\nEnergy avaliable: {eco.energy_avaliable}" +
            f"\nSimulation speed: {simulation_speed}x" +
            f"\nSimulation time: {round(self.simulation_time)} seconds")
        print("-----------------------")


    def on_mouse_press(self, x, y: int, button, modifiers):
        for organism in self.organisms:
            if organism.collides_with_point((x, y)):
                organism.print_info()

    def on_key_press(self, key, modifiers):
        global simulation_speed
        if key == arcade.key.I:
            self.show_panel = not self.show_panel
            self.print_info_simulation()

        if key == arcade.key.RIGHT:
            if simulation_speed >= 1:
                simulation_speed += 1
            elif simulation_speed == 0.5:
                simulation_speed = 1
            elif simulation_speed == 0.25:
                simulation_speed = 0.5
            print(f"Simulation speed updated to {simulation_speed}x")
        if key == arcade.key.LEFT:
            if simulation_speed >= 2:
                simulation_speed -= 1
                print(f"Simulation speed updated to {simulation_speed}x")
            elif simulation_speed == 1:
                simulation_speed = 0.5
                print(f"Simulation speed updated to {simulation_speed}x")
            elif simulation_speed == 0.5:
                simulation_speed = 0.25
                print(f"Simulation speed updated to {simulation_speed}x")
            else:
                print(f"Simulation speed is at the minimum of {simulation_speed}x")

    def create_organisms(self):
        global organism_name
        for i in range(STARTING_POPULATION):
            organism = Organism("assets/organism_sprite.png", ORGANISM_SCALING)
            organism.center_x = random.randrange(64, WIDTH_SIZE-64)
            organism.center_y = random.randrange(64, HEIGHT_SIZE-64)
            organism.name = organism_name
            if START_WITH_MUTATION:
                organism.mutation()
            self.organisms.append(organism)
            organism_name += 1

    def spawn_offspring(self, offspring):
        self.organisms.append(offspring)

    def check_if_dead(self):
        for organism in self.organisms:
            if organism.alive == False:
                organism.remove_from_sprite_lists()
                

def main():
    global simulation
    global organism_name
    global simulation_speed
    organism_name = 1
    simulation_speed = 1
    simulation = Simulation(WIDTH_SIZE, HEIGHT_SIZE, "LifeBox Simulator")
    simulation.setup()
    arcade.run()

if __name__ == "__main__":
    main()
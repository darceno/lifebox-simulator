import pygame
import random
import time

from settings import *
from debug import debug

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("LifeBox Simulator")
clock = pygame.time.Clock()


# Organisms class
class Organism:
    def __init__(self, x, y, color, genome):
        self.x = x
        self.y = y
        self.color = color
        self.decision = None
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.last_decision = 0
        self.genome = genome
        self.size = len(self.genome) * SIZE_BY_GENE
        self.energy = 1
        self.nutrients = 0
        self.last_birthday = self.last_cellular_respiration = time.time()
        self.age = 0
        self.alive = True

    def draw(self):
        rect_x = self.x - self.size
        rect_y = self.y - self.size
        rect_width = rect_height = self.size * 2
        self.rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        rect_surface = pygame.Surface((rect_width, rect_width), pygame.SRCALPHA)
        screen.blit(rect_surface, (rect_x, rect_y))
        pygame.draw.rect(rect_surface, (255, 0, 0, 255), self.rect)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move_decision(self):
        self.decision = random.randint(0, 7) # 0/right - 1/left - 2/down - 3/up - 4/right-down - 5/right-up - 6/left-down - 7/left-up
        decision_options = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        self.decision_delay = random.choice(decision_options)
        self.last_decision = time.time()

    def move(self):
        if self.last_decision == 0:
            self.move_decision()
        if time.time() - self.last_decision > self.decision_delay:
            self.move_decision()
        if self.decision == 0 and self.x + SPEED < WIDTH_SIZE-self.size: #right
            self.x += SPEED * dt
        elif self.decision == 1 and self.x - SPEED > 20: #left
            self.x -= SPEED * dt
        elif self.decision == 2 and self.y + SPEED < HEIGHT_SIZE-self.size: #down
            self.y += SPEED * dt
        elif self.decision == 3 and self.y - SPEED > self.size: #up
            self.y -= SPEED * dt
        elif self.decision == 4 and self.x + SPEED < WIDTH_SIZE-self.size and self.y + SPEED < HEIGHT_SIZE-self.size: #right-down
            self.x += SPEED * dt
            self.y += SPEED * dt
        elif self.decision == 5 and self.x + SPEED < WIDTH_SIZE-self.size and self.y - SPEED > self.size: #right-up
            self.x += SPEED * dt
            self.y -= SPEED * dt
        elif self.decision == 6 and self.x - SPEED > self.size and self.y + SPEED < HEIGHT_SIZE-self.size: #left-down
            self.x -= SPEED * dt
            self.y += SPEED * dt
        elif self.decision == 7 and self.x - SPEED > self.size and self.y - SPEED > self.size: #left-up
            self.x -= SPEED * dt
            self.y -= SPEED * dt
        else:
            self.move_decision()

    def cellular_respiration(self):
        if time.time() - self.last_cellular_respiration > 1:
            energy_consumption = len(self.genome) + 3
            nutrients_variation = random.randint(7, 13)
            self.nutrients += nutrients_variation - energy_consumption
            self.last_cellular_respiration = time.time()

    def energy_conversion(self):
        if self.nutrients >= 30:
            self.energy += 1
            self.nutrients -= 30
            self.energy_conversion()      
    
    def asexual_reproduction(self):
        if self.energy >= len(self.genome) + 1:
            if random.randint(1, 10) >= 5:
                self.offspring_birth_location()
                offspring = Organism(self.offspring_x, self.offspring_y, "blue", self.genome)
                simulation.spawn_offsprings(offspring)
                self.energy -= len(self.genome)
            else:
                self.energy -= self.energy//2

    def offspring_birth_location(self):
        self.offspring_x = self.x
        self.offspring_y = self.y
        x_direction = random.randint(1, 3)
        y_direction = random.randint(1, 3)
        if x_direction == 1:
            self.offspring_x = self.x + self.size * 3
            if self.offspring_x >= WIDTH_SIZE - self.size:
                self.offspring_x = self.x - self.size * 3
        if x_direction == 2:
            self.offspring_x = self.x - self.size * 3
            if self.offspring_x <= self.size:
                self.offspring_x = self.x + self.size * 3
        else:
            pass 
        if y_direction == 1:
            self.offspring_y = self.y + self.size * 3
            if self.offspring_y >= WIDTH_SIZE - self.size:
                self.offspring_y = self.y - self.size * 3
        if y_direction == 2:
            self.offspring_y = self.y - self.size * 3
            if self.offspring_y <= self.size:
                self.offspring_y = self.y + self.size * 3
        else:
            pass

    def aging(self):
        if time.time() - self.last_birthday > YEAR:
            self.age += 1
            self.last_birthday = time.time()
        if self.age == len(self.genome):
            self.alive = False

    def universal_abilities(self):
        self.draw()
        self.aging()
        self.energy_conversion()

    def genetic_abilities(self):
        if "CR" in self.genome:
            self.cellular_respiration()
        if "RA" in self.genome:
           self.asexual_reproduction()
        if "MM" in self.genome:
            self.move()

    def collision_abilities(self, organism2):
        pass


# Simulation main class
class Main:
    def __init__(self):
        self.organisms = []
        self.alive_organisms = []
        self.first_generation = True
        self.time = time.time()

    def create_organisms(self):
        if self.first_generation:
            for i in range(STARTING_POPULATION):
                organism = Organism(random.randint(20, WIDTH_SIZE-20), random.randint(20, HEIGHT_SIZE-20), STARTING_COLOR, ["CR", "RA"])
                self.organisms.append(organism)
            self.first_generation = False
                             
    def spawn_offsprings(self, offspring):
        self.organisms.append(offspring)
    
    def check_if_alive(self):
        for i in range(len(self.organisms)):
            if self.organisms[i].alive == True:
                self.alive_organisms.append(self.organisms[i])
        self.organisms = self.alive_organisms
        self.alive_organisms = []
    
    def check_collisions(self):
        for i in range(len(self.organisms)):
            for j in range(i+1, len(self.organisms)):
                if self.organisms[i].rect.colliderect(self.organisms[j].rect):
                    self.organisms[i].collision_abilities(self.organisms[j])

    def info_display(self):
        current_time = time.time() - self.time
        self.font = pygame.font.SysFont(None, font_size)
        self.population = len(self.organisms)
        self.frames = int(clock.get_fps())
        FPS_counter = self.font.render(f"FPS: {self.frames}",  anti_aliasing, font_color)
        population_counter = self.font.render(f"Current population: {self.population}", anti_aliasing, font_color)
        simulation_time = self.font.render(f"Simulation time: {'%.1f' % (current_time)} sec", anti_aliasing, font_color)
        if show_FPS:
            screen.blit(FPS_counter, (10, 10))
        if show_population and show_FPS:
            screen.blit(population_counter, (10, 10 + font_size))
        if show_population and not show_FPS:
            screen.blit(population_counter, (10, 10))
        if show_time and show_FPS and show_population:
            screen.blit(simulation_time, (10, 10 + (font_size*2)))
        if show_time and show_population and not show_FPS:
            screen.blit(simulation_time, (10, 10 + font_size))
        if show_time and show_FPS and not show_population:
            screen.blit(simulation_time, (10, 10 + font_size))
        if show_time and not show_population and not show_FPS:
            screen.blit(simulation_time, (10, 10))

    def update_screen(self):
        for organism in self.organisms:
            organism.universal_abilities()
            organism.genetic_abilities()
        self.check_collisions()
        self.check_if_alive()

        #debug("info")

        pygame.display.update()


# Pygame game loop
run = True
simulation = Main()
previous_frame_time = time.time()
pause = False

while run:
    clock.tick(FPS)
    dt = time.time() - previous_frame_time
    previous_frame_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

    if not pause:
        simulation.create_organisms()
        if enable_info_display:
            simulation.info_display()
        simulation.update_screen()

    screen.fill(BG_COLOR)

pygame.quit()
import pygame
import random

from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("LifeBox Simulator")
clock = pygame.time.Clock()

# Organisms class
class Organism:
    def __init__(self, x, y, color, genome, size=STARTING_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.decision = None
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.last_decision = 0
        self.genome = genome
        self.energy = 1
        self.nutrients = 0
        self.last_birthday = 0
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
        self.decision = random.randrange(8) # 0/right - 1/left - 2/down - 3/up - 4/right-down - 5/right-up - 6/left-down - 7/left-up
        self.decision_delay = random.randint(5, 60)
        self.last_decision = 0

    def move(self):
        self.last_decision += 1
        if self.decision == 0 and self.x + SPEED < WIDTH_SIZE-self.size: #right
            self.x += SPEED
        elif self.decision == 1 and self.x - SPEED > 20: #left
            self.x -= SPEED
        elif self.decision == 2 and self.y + SPEED < HEIGHT_SIZE-self.size: #down
            self.y += SPEED
        elif self.decision == 3 and self.y - SPEED > self.size: #up
            self.y -= SPEED
        elif self.decision == 4 and self.x + SPEED < WIDTH_SIZE-self.size and self.y + SPEED < HEIGHT_SIZE-self.size: #right-down
            self.x += SPEED
            self.y += SPEED
        elif self.decision == 5 and self.x + SPEED < WIDTH_SIZE-self.size and self.y - SPEED > self.size: #right-up
            self.x += SPEED
            self.y -= SPEED
        elif self.decision == 6 and self.x - SPEED > self.size and self.y + SPEED < HEIGHT_SIZE-self.size: #left-down
            self.x -= SPEED
            self.y += SPEED
        elif self.decision == 7 and self.x - SPEED > self.size and self.y - SPEED > self.size: #left-up
            self.x -= SPEED
            self.y -= SPEED
        else:
            self.move_decision()
        if self.last_decision > self.decision_delay:
            self.move_decision()
            self.last_decision = 0

    def CR_energy_balance(self):
        self.hunger = 0
        self.hunger += len(self.genome)
        nutrients_variation = random.randint(3, 9)
        self.nutrients += nutrients_variation - self.hunger
        if self.nutrients >= 1000:
            self.energy += 1
            self.nutrients = 0
    
    def asexual_reproduction(self):
        if self.energy >= len(self.genome) + 1:
            if random.randint(1, 2) == 2:
                offspring = Organism(self.x, self.y, "blue", self.genome)
                simulation.spawn_offsprings(offspring)
                self.energy -= len(self.genome)
            else:
                self.energy -= self.energy//2

    def aging(self):
        self.last_birthday += 1
        if self.last_birthday >= 100:
            self.age += 1
            self.last_birthday = 0
        if self.age > len(self.genome):
            self.alive = False

    def universal_abilities(self):
        self.draw()
        self.aging()

    def genetic_abilities(self):
        self.move()
        if "CR" in self.genome:
            self.CR_energy_balance()
        if "RA" in self.genome:
           self.asexual_reproduction()

    def collision_abilities(self, organism2):
        pass

# Simulation main class
class Main:
    def __init__(self):
        self.organisms = []
        self.alive_organisms = []
        self.first_generation = True


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
        self.font = pygame.font.SysFont(None, font_size)
        self.population = len(self.organisms)
        self.frames = int(clock.get_fps())
        FPS_counter = self.font.render(f"FPS: {self.frames}",  anti_aliasing, font_color)
        population_counter = self.font.render(f"Current population: {self.population}", anti_aliasing, font_color)
        if show_FPS:
            screen.blit(FPS_counter, (10, 10))
        if show_population and show_FPS:
            screen.blit(population_counter, (10, font_size))
        if show_population and not show_FPS:
            screen.blit(population_counter, (10, 10))

    def update_screen(self):
        for organism in self.organisms:
            organism.universal_abilities()
            organism.genetic_abilities()
        self.check_collisions()
        self.check_if_alive()

        pygame.display.update()

# Pygame game loop
run = True
simulation = Main()
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    simulation.create_organisms()
    if enable_info_display:
        simulation.info_display()
    simulation.update_screen()

    screen.fill(BG_COLOR)


pygame.quit()
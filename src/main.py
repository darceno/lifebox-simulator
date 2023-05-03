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
        if self.decision == 0 and self.x < WIDTH_SIZE-self.size: #right
            self.x += SPEED
        elif self.decision == 1 and self.x > 20: #left
            self.x -= SPEED
        elif self.decision == 2 and self.y < HEIGHT_SIZE-self.size: #down
            self.y += SPEED
        elif self.decision == 3 and self.y > self.size: #up
            self.y -= SPEED
        elif self.decision == 4 and self.x < WIDTH_SIZE-self.size and self.y < HEIGHT_SIZE-self.size: #right-down
            self.x += SPEED
            self.y += SPEED
        elif self.decision == 5 and self.x < WIDTH_SIZE-self.size and self.y > self.size: #right-up
            self.x += SPEED
            self.y -= SPEED
        elif self.decision == 6 and self.x > self.size and self.y < HEIGHT_SIZE-self.size: #left-down
            self.x -= SPEED
            self.y += SPEED
        elif self.decision == 7 and self.x > self.size and self.y > self.size: #left-up
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
        self.nutrients += 11 - self.hunger
        if self.nutrients >= 1000:
            self.energy += 1
            self.nutrients = 0

    def universal_abilities(self):
        self.draw()

    def genetic_abilities(self):
        self.move()
        if "CR" in self.genome:
            self.CR_energy_balance()

    def collision_abilities(self, organism2):
        pass

# Simulation main class
class Main:
    def __init__(self):
        self.organisms = []

    def create_organisms(self):
        if len(self.organisms) == 0:
            for i in range(STARTING_POPULATION):
                organism = Organism(random.randint(20, WIDTH_SIZE-20), random.randint(20, HEIGHT_SIZE-20), STARTING_COLOR, ["CR", "RA"])
                self.organisms.append(organism)                
    
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
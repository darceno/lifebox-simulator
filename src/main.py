import pygame
import random

# Simulaiton settings
WIDTH_SIZE, HEIGHT_SIZE = 1000, 500
FPS = 30
SPEED = 1
BG_COLOR = (21, 36, 36)
INITIAL_POPULATION = 10

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("LifeBox Simulator")
clock = pygame.time.Clock()

# Organisms class
class Organism:
    def __init__(self, x, y, color, size=7, genome=["CR", "RA"]):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.decision = None
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.last_decision = 0
        self.genome = genome
        self.energy = 3
        self.hunger = 0

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

    def energy_consumption(self):
        self.hunger += 1
        if self.hunger >= 300:
            self.energy -= 1
            self.hunger = 0

# Simulation main class
class Main:
    def __init__(self):
        self.organisms = []

    def create_organisms(self):
        if len(self.organisms) == 0:
            for i in range(INITIAL_POPULATION):
                organism = Organism(random.randint(20, WIDTH_SIZE-20), random.randint(20, HEIGHT_SIZE-20), "white")
                self.organisms.append(organism)                
    
    def check_collisions(self):
        for i in range(len(self.organisms)):
            for j in range(i+1, len(self.organisms)):
                if self.organisms[i].rect.colliderect(self.organisms[j].rect):
                    print("collision")
    
    def update_screen(self):
        for organism in self.organisms:
            organism.draw()
            organism.move()
            organism.energy_consumption()
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
    simulation.update_screen()

    screen.fill(BG_COLOR)


pygame.quit()
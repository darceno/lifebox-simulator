import pygame, random

# Simulaiton settings
WIDTH_SIZE, HEIGHT_SIZE = 1000, 500
FPS = 60
SPEED = 2

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Cell Simulation")
clock = pygame.time.Clock()

# Organisms parent class
class ORGANISM:
    def __init__(self, x, y, color, size=15):
        self.x = random.randint(20, WIDTH_SIZE-20)
        self.y = random.randint(20, HEIGHT_SIZE-20)
        self.size = size
        self.color = color
        self.decision = None

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move_decision(self):
        self.decision = random.randrange(8) # 0/right - 1/left - 2/down - 3/up - 4/right-down - 5/right-up - 6/left-down - 7/left-up
        self.decision_delay = random.randint(5, 60)

    def move(self):
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

# Simulation main loop
def main():
    run = True
    organisms = []
    population = 10
    frame_count = 0

    def update_screen():
        nonlocal frame_count
        frame_count += 1

        if len(organisms) == 0:
            for i in range(population):
                organism = ORGANISM(WIDTH_SIZE/2, HEIGHT_SIZE/2, "white")
                organisms.append(organism)

        for organism in organisms:
            organism.draw()
            organism.move()
            if frame_count > organism.decision_delay:
                organism.move_decision()

        if frame_count > organism.decision_delay:
            frame_count = 0
        
        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill("darkslategray")
        update_screen()

    pygame.quit()

if __name__ == "__main__":
    main()
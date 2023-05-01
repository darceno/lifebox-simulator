import pygame, random

# Simulaiton settings
WIDTH_SIZE, HEIGHT_SIZE = 1000, 500
FPS = 60
SPEED = 2
BG_COLOR = (21, 36, 36)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Cell Simulation")
clock = pygame.time.Clock()

# Organisms parent class
class ORGANISM:
    def __init__(self, x, y, color, size=10):
        self.x = random.randint(20, WIDTH_SIZE-20)
        self.y = random.randint(20, HEIGHT_SIZE-20)
        self.size = size
        self.color = color
        self.decision = None
        self.rect = pygame.Rect(self.x, self.y, 1, 1)

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

    def update_screen():

        if len(organisms) == 0:
            for i in range(population):
                organism = ORGANISM(WIDTH_SIZE/2, HEIGHT_SIZE/2, "white")
                organisms.append(organism)

        for organism in organisms:
            organism.draw()
            organism.move()
            organism.last_decision += 1
            if organism.last_decision > organism.decision_delay:
                organism.move_decision()
                organism.last_decision = 0

        for i in range(len(organisms)):
            for j in range(i+1, len(organisms)):
                if organisms[i].rect.colliderect(organisms[j].rect):
                    pass
        
        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(BG_COLOR)
        update_screen()

    pygame.quit()

if __name__ == "__main__":
    main()
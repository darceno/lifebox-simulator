import pygame
import random

# Simulaiton settings
WIDTH_SIZE, HEIGHT_SIZE = 1000, 500
FPS = 60

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

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size) 

# Simulation main loop
def main():
    run = True

    def update_screen():
        screen.fill("darkslategray")
        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        update_screen()

    pygame.quit()

if __name__ == "__main__":
    main()
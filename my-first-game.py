import pygame
import random
import math
import colorsys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Fancy Particle Playground")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):

        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 7)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(60, 120)
        self.max_life = self.life

        self.size = random.uniform(4, 8)

        self.hue = random.random()

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.05
        self.vx *= 0.995
        self.vy *= 0.995

        self.life -= 1
        self.size *= 0.98

        self.hue += 0.01

    def draw(self, surf):

        if self.life <= 0:
            return

        rgb = colorsys.hsv_to_rgb(self.hue % 1, 0.8, 1)
        color = tuple(int(c * 255) for c in rgb)

        alpha = int(255 * (self.life / self.max_life))

        glow_surf = pygame.Surface((50, 50), pygame.SRCALPHA)

        pygame.draw.circle(
            glow_surf,
            (*color, alpha//4),
            (25,25),
            int(self.size*3)
        )

        surf.blit(glow_surf, (self.x-25, self.y-25))

        pygame.draw.circle(
            surf,
            color,
            (int(self.x), int(self.y)),
            int(self.size)
        )

    def alive(self):
        return self.life > 0


def draw_background(surface, t):

    for y in range(HEIGHT):

        r = int(20 + 20 * math.sin(y*0.02 + t))
        g = int(40 + 30 * math.sin(y*0.01 + t*0.7))
        b = int(80 + 40 * math.sin(y*0.015 + t*0.4))

        pygame.draw.line(surface, (r,g,b), (0,y), (WIDTH,y))


running = True
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:
        for _ in range(12):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.03

    draw_background(screen, time)

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
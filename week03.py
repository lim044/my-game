import pygame
 
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

x, y = 400, 300
dx, dy = 5, 5
speed = 99
radius = 30

mode = "control"  # control / auto

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

        # 🔥 우클릭 → 멈추고 다시 조작
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 3:
                mode = "control"
                dx, dy = 0, 0  # 멈춤

    keys = pygame.key.get_pressed()

    # 🕹️ 조작 모드
    if mode == "control":
        if keys[pygame.K_w]:
            y -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_d]:
            x += speed

    # 🤖 자동 모드 (튕김)
    elif mode == "auto":
        x += dx
        y += dy

    # 🔥 벽 충돌 체크
    hit_wall = False

    if x <= radius:
        x = radius
        hit_wall = True
    if x >= 800 - radius:
        x = 800 - radius
        hit_wall = True
    if y <= radius:
        y = radius
        hit_wall = True
    if y >= 600 - radius:
        y = 600 - radius
        hit_wall = True

    # 🔥 벽에 닿으면 자동 모드로 전환 + 튕기기
    if hit_wall and mode == "control":
        mode = "auto"

        # 방향 결정 (간단 버전)
        dx = 5 if x <= radius else -5
        dy = 5 if y <= radius else -5

    # 🔥 자동 모드에서는 반사
    if mode == "auto":
        if x <= radius or x >= 800 - radius:
            dx = -dx
        if y <= radius or y >= 600 - radius:
            dy = -dy

    screen.fill((255, 255, 255))

    # 모드에 따라 색 변경
    if mode == "control":
        color = (0, 0, 255)  # 빨강 (조작 중)
    else:
        color = (255, 0, 0)  # 파랑 (자동)

    pygame.draw.circle(screen, color, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

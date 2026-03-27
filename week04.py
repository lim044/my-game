import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# 색상
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 플레이어
player_rect = pygame.Rect(100, 100, 60, 60)
player_angle = 0
speed = 5

# 중앙 박스
box_center = (WIDTH // 2, HEIGHT // 2)
box_size = 100
box_angle = 0

# 충돌 모드
mode = 0
mode_names = ["AABB", "OBB", "Circle"]

# -----------------------------
# OBB 함수
# -----------------------------
def get_obb_points(center, w, h, angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    corners = [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
    points = []

    for x,y in corners:
        rx = x*cos_a - y*sin_a
        ry = x*sin_a + y*cos_a
        points.append((rx+center[0], ry+center[1]))
    return points

def normalize(v):
    length = math.hypot(v[0], v[1])
    return (0,0) if length == 0 else (v[0]/length, v[1]/length)

def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1)%len(points)]
        edge = (p2[0]-p1[0], p2[1]-p1[1])
        normal = (-edge[1], edge[0])
        axes.append(normalize(normal))
    return axes

def project(points, axis):
    dots = [p[0]*axis[0] + p[1]*axis[1] for p in points]
    return min(dots), max(dots)

def overlap(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

def sat_collision(p1, p2):
    axes = get_axes(p1) + get_axes(p2)
    for axis in axes:
        if not overlap(project(p1, axis), project(p2, axis)):
            return False
    return True

# -----------------------------
# 게임 루프
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 좌클릭 → 모드 변경
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mode = (mode + 1) % 3

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_a]:
        player_rect.x -= speed
    if keys[pygame.K_d]:
        player_rect.x += speed
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed

    # 회전
    rotation_speed = 5 if keys[pygame.K_z] else 1
    box_angle += rotation_speed
    player_angle += 1

    # -----------------------------
    # 충돌 계산
    # -----------------------------
    box_aabb = pygame.Rect(
        box_center[0] - box_size//2,
        box_center[1] - box_size//2,
        box_size, box_size
    )

    player_center = player_rect.center
    player_r = player_rect.width // 2
    box_r = box_size // 2

    dx = player_center[0] - box_center[0]
    dy = player_center[1] - box_center[1]

    player_points = get_obb_points(player_center, player_rect.width, player_rect.height, player_angle)
    box_points = get_obb_points(box_center, box_size, box_size, box_angle)

    # 선택된 충돌
    hit = False

    if mode == 0:
        hit = player_rect.colliderect(box_aabb)
    elif mode == 1:
        hit = sat_collision(player_points, box_points)
    elif mode == 2:
        hit = (dx*dx + dy*dy) < ((player_r + box_r)**2)

    # 배경
    screen.fill((255, 255, 100) if hit else WHITE)

    # -----------------------------
    # 항상 보이는 오브젝트
    # -----------------------------
    pygame.draw.rect(screen, GRAY, player_rect)
    pygame.draw.rect(screen, GRAY, box_aabb)

    # -----------------------------
    # 선택된 충돌 표시
    # -----------------------------
    if mode == 0:  # AABB
        pygame.draw.rect(screen, RED, player_rect, 2)
        pygame.draw.rect(screen, RED, box_aabb, 2)

    elif mode == 1:  # OBB
        pygame.draw.polygon(screen, GREEN, player_points, 2)
        pygame.draw.polygon(screen, GREEN, box_points, 2)

    elif mode == 2:  # Circle
        pygame.draw.circle(screen, BLUE, player_center, player_r, 2)
        pygame.draw.circle(screen, BLUE, box_center, box_r, 2)

    # 텍스트
    text = font.render(f"Mode: {mode_names[mode]} | {'HIT' if hit else 'MISS'}", True, (0,0,0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
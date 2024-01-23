import pygame
from map import Map
from Car import Car

# generate random points to get a map
pygame.init()
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")
car = Car()
level_map = Map('./level.json')
clock = pygame.time.Clock()


# pygame.draw.circle(win, (0, 255, 0), points[0], 5)
def update():
    win.fill((0, 0, 0))
    level_map.draw(win)
    car.draw(win)
    car.move(pygame.key.get_pressed())
    car.lidar(win, level_map)
    level_map.check_reward(car.position)
    if is_collided := car.check_collision(level_map):
        print("collided")
    pygame.display.flip()


run = True
# keys = pygame.key.get_pressed()
while run:
    update()
    clock.tick(60)
    if pygame.mouse.get_pressed()[0]:
        print(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

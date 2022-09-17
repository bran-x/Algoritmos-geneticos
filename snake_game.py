import pygame
from controller import GeneticAlgorithm
pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption('Snake game')

color_white = [255, 255, 255]
color_gray = [70, 70, 70]
color_green = [0,255,0]
color_black = [0,0,0]
color_red = [255,0,0]

font_basic = pygame.font.SysFont('arial', 16)

def drawBoard(screen):
    screen.fill(color_white)
    pygame.draw.rect(screen, color_gray, [540, 0, 180, 480])

def drawWalls(screen):
    pygame.draw.rect(screen, color_green, [0, 0, 20, 480])
    pygame.draw.rect(screen, color_green, [520, 0, 20, 480])
    pygame.draw.rect(screen, color_green, [0, 0, 540, 20])
    pygame.draw.rect(screen, color_green, [0, 460, 540, 20])

def drawSnake(screen, snake):
    for block in snake.body:
        x, y = block[0], block[1]
        pygame.draw.rect(screen, color_black, [x, y, 10, 10])
    x, y = snake.food_pos
    pygame.draw.rect(screen, color_red, [x, y, 10, 10])

def drawInfo(screen, info):
    gen = info['gen']
    pop = info['pop']
    bf = info['bf']/1000
    tf = info['tf']/1000
    text1 = font_basic.render('Generation: '+str(gen), True, color_white)
    screen.blit(text1, [550, 30])
    text1 = font_basic.render('Population: '+str(pop), True, color_white)
    screen.blit(text1, [550, 50])
    text1 = font_basic.render('Best Fitness: '+str(bf), True, color_white)
    screen.blit(text1, [550, 70])
    text1 = font_basic.render('Total Fitness: '+str(tf), True, color_white)
    screen.blit(text1, [550, 90])

# Controller
ctrl = GeneticAlgorithm(800, 250)

finish = False
training = True
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    drawBoard(screen)
    drawWalls(screen)
    if training:
        snake, info = ctrl.update()
        status = info['status']
        if status == 'train':
            drawSnake(screen, snake)
        else:
            training = False
    else:
        ctrl.play_snake(snake)
        drawSnake(screen, snake)
        if snake.died or snake.lifetime>100*(len(snake.body)-2):
            ctrl.next_gen()
            training = True

    drawSnake(screen,snake)
    drawInfo(screen, info)
    pygame.display.update()
    fpsClock.tick(30)

pygame.quit()
quit()

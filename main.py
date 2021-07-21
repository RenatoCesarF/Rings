import pygame


pygame.init()
SCREEN_WITH = 800
SCREEN_HEIGHT = 400
FONT = pygame.font.Font("res/Pixellari.ttf", 30)

screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()


def getMousePosition():
    pos = pygame.mouse.get_pos()
    return (pos)

def writeInScreen(text,destiny, position):
    interface_surface = FONT.render(text, False, "White")
    destiny.blit(interface_surface,position)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    writeInScreen("anything",screen,(0,0))
    pygame.display.update()
    clock.tick(60)



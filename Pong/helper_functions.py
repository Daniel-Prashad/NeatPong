import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0,0,0)
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
PAUSE_FONT = pygame.font.SysFont("impact", 100)
pygame.display.set_caption("PONG")


def countdown():
    '''() -> Nonetype
    This function is used to display a countdown before starting a game so that the player(s) can prepare.
    '''
    # set the font for the countdown
    count_down_font = pygame.font.SysFont("impact", 100)
    # display the countdown
    for i in range(3, -1, -1):
        WIN.fill(BLACK)
        if i == 0:
            text = count_down_font.render("START!", 1, WHITE)
        else:
            text = count_down_font.render(f"{i}", 1, WHITE)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(1000)


def pause(WIN):
    '''(Window) -> Nonetype
    This function is used to pause the game.
    '''
    pause_text = PAUSE_FONT.render("PAUSED", 1, (160, 160, 160))
    WIN.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - pause_text.get_height()//2))
    pygame.display.update()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

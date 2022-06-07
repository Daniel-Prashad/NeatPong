from Pong.game import Game
from Pong.pong_neat_ai import PongNeatAI
from Pong.pong_neat_ai import run_neat

import neat
import os
import pickle
import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0,0,0)
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")


def get_config():
    '''() -> config
    This function is used to get the configuration file used to train the AI to play Pong.
    '''
    # define the file path for the configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "pong_neat_config.txt")
    # define the properties from the configuration file that will be used
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    return(config)


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


def display_title_screen(config):
    '''(config) -> Nonetype
    This function is used to display the title screen of the game, as well as navigate to and from description screen of each game mode.
    '''
    # set the background colour as black and the title and regular text fonts
    WIN.fill(BLACK)
    title_font = pygame.font.SysFont("verdana", 75)
    text_font = pygame.font.SysFont("verdana", 16)
    
    # store all of th text for the title screen
    title_text = title_font.render("PONG", 1, WHITE)
    text1 = text_font.render("Please press the corresponding key to play the game mode of your choice:", 1, WHITE)
    option0_text = text_font.render("[0] - Watch the NEAT algorithm run to train the AI to play", 1, WHITE)
    option1_text = text_font.render("[1] - Play a basic single-player game", 1, WHITE)
    option2_text = text_font.render("[2] - Play a two-player game", 1, WHITE)
    option3_text = text_font.render("[3] - Play a single-player game against the AI trained using the NEAT algorithm", 1, WHITE)

    # display the text on the title screen
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    WIN.blit(text1, (20, 160))
    WIN.blit(option0_text, (20, 200))
    WIN.blit(option1_text, (20, 240))
    WIN.blit(option2_text, (20, 280))
    WIN.blit(option3_text, (20, 320))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            # if the user closes the window, quit the game
            if event.type == pygame.QUIT:
                run = False
                quit()
            # otherwise, display the description for the game mode depending on the user's selection
            # and continue with the selected game if they so choose
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_0]:
                    display_game_mode_screen(0)
                    run_neat(config)
                elif keys[pygame.K_1]:
                    game = Game(WIN, WIDTH, HEIGHT, 1)
                    display_game_mode_screen(1)
                    game.play_game()
                elif keys[pygame.K_2]:
                    game = Game(WIN, WIDTH, HEIGHT, 2)
                    display_game_mode_screen(2)
                    game.play_game()
                elif keys[pygame.K_3]:
                    with open("winner.pickle", "rb") as f:
                        winner = pickle.load(f)
                    game = PongNeatAI(WIN, WIDTH, HEIGHT, 3)
                    display_game_mode_screen(3)
                    game.play_ai(winner, config)
               

def display_game_mode_screen(game_mode):
    '''(int) -> Nonetype
    This function is used to display the description of the game mode selected by the user.
    It allows the user to either continue with their choice or return to the main menu.
    '''
    # set the background colour as black and the title and regular text fonts
    WIN.fill(BLACK)
    title_font = pygame.font.SysFont("verdana", 30)
    text_font = pygame.font.SysFont("verdana", 16)

    # store the title and description texts depending on the selected game mode
    if game_mode == 0:
        title_text = title_font.render("0 - TRAINING WITH NEAT", 1, WHITE)
        description_text1 = text_font.render("Watch as the NEAT algorithm trains the AI to play PONG.", 1, WHITE)
        description_text2 = text_font.render("Once completed, the AI will automatically be stored.", 1, WHITE)
        description_text3 = text_font.render("Try playing against it by selecting option 3 in the main menu.", 1, WHITE)
    elif game_mode == 1:
        title_text = title_font.render("1 - BASIC SINGLE-PLAYER GAME", 1, WHITE)
        description_text1 = text_font.render("Play a single-player game where the opposing paddle simply tracks the ball.", 1, WHITE)
        description_text2 = text_font.render("This may seem difficult at first, but there is a huge exploit. Can you find it?", 1, WHITE)
        description_text3 = text_font.render("First to 5 points wins!", 1, WHITE)
    elif game_mode == 2:
        title_text = title_font.render("2 - TWO-PLAYER GAME", 1, WHITE)
        description_text1 = text_font.render("Play a two-player game.", 1, WHITE)
        description_text2 = text_font.render("Left player controls: [W] & [S] \ Right player controls: [UP] & [DOWN]", 1, WHITE)
        description_text3 = text_font.render("First to 5 points wins!", 1, WHITE)
    elif game_mode == 3:
        title_text = title_font.render("3 - SINGLE PLAYER GAME AGAINST AI", 1, WHITE)
        description_text1 = text_font.render("Play a single-player game against the AI trained using the NEAT algorithm.", 1, WHITE)
        description_text2 = text_font.render("First to 5 points wins!", 1, WHITE)
        description_text3 = text_font.render("(Spoiler: You won't win)", 1, WHITE)
    return_text = text_font.render("[ESC] - Return to the title screen", 1, WHITE)
    continue_text = text_font.render("[ENTER] - Continue", 1, WHITE)
    
    # display the text on the screen
    WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))
    WIN.blit(description_text1, (20, 180))
    WIN.blit(description_text2, (20, 220))
    WIN.blit(description_text3, (20, 260))
    WIN.blit(return_text, (20, 460))
    WIN.blit(continue_text, (520, 460))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            # if the user closes the window, quit the game
            if event.type == pygame.QUIT:
                run = False
                quit()
            # otherwise, depending on the user's input, either return to the main menu or continue to the selected game
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    config = get_config()
                    display_title_screen(config)
                elif keys[pygame.K_RETURN]:
                    run = False
    countdown()


if __name__ == '__main__':
    config = get_config()
    display_title_screen(config)





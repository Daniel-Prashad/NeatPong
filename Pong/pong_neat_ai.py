from .paddle import Paddle
from .helper_functions import pause
from .game import Game

import pygame
import neat
import pickle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def evaluate_genomes(genomes, config):
    '''(genomes, config) -> Nonetype
    This function is used to evaluate the fitness of each genome.
    '''
    # genomes is a list of tuples where each has the genome_id and genome object 
    # each genome plays every single other genome one time
    # the fitness of each genome is the sum of each fitness of each game played
    for i, (genome_id1, genome1) in enumerate(genomes):
        # initialize the fitness of genome1
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            # initialize fitness of genome2 upon creation, when it plays for the first time
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            # start a game and allow genome1 and genome2 play
            game = PongNeatAI(WIN, WIDTH, HEIGHT, 0)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    '''(config) -> Nonetype
    This function is used to run the NEAT algorithm and store the winning genome.
    '''
    # set up the population using the configuration file
    pop = neat.Population(config)
    # add data to the standard output so that the current generation, best fitness, average fitness, etc can be displayed
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    # save a checkpoint after every 1 generation, allows to restart the algorithm from a checkpoint
    # in order to load from a checkpoint, use:
    # >> pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
    # instead of 
    # >> pop = neat.Population(config)
    pop.add_reporter(neat.Checkpointer(1))
    # run the evualte_genomes function 50 times and store the highest-scoring genome
    winner = pop.run(evaluate_genomes, 50)
    # save the winning genome
    with open("winner.pickle", "wb") as f:
        pickle.dump(winner, f)
    # let the user know that the training has been completed
    display_completed_training_screen(winner, config)


def display_completed_training_screen(winner, config):
    '''(genome, config) -> Nonetype
    This function is used to notify the user that the training has been completed and
    gives the user of playing a game against the AI.
    '''
    # notify the user that the training is complete and prompt the user to start a game against the AI
    WIN.fill(BLACK)
    text_font = pygame.font.SysFont("verdana", 20)
    text1 = text_font.render("The training has been completed!", 1, WHITE)
    text2 = text_font.render("You can now load in the AI using option 3 from the main menu.", 1, WHITE)
    text3 = text_font.render("Please press [ENTER] to begin a game against the AI now.", 1, WHITE)
    text4 = text_font.render("First to 5 points wins!", 1, WHITE)
    WIN.blit(text1, (20, 160))
    WIN.blit(text2, (20, 200))
    WIN.blit(text3, (20, 240))
    WIN.blit(text4, (20, 280))
    pygame.display.update()

    # begin the game against the AI once the user presses the [ENTER] key
    run = True
    while run:
        for event in pygame.event.get():
            # if the user closes the window, quit the game
            if event.type == pygame.QUIT:
                run = False
                quit()
            # begin the game against the AI once the user presses the [ENTER] key
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    game = PongNeatAI(WIN, WIDTH, HEIGHT, 3)
                    game.play_ai(winner, config)


class PongNeatAI:
    '''This class is used to train the AI to play Pong.'''

    def __init__(self, window, width, height, game_mode):
        '''(PongNeatAI, Window, int, int, int) -> Nonetype
        This function sets up a game of Pong to be used to train the AI.
        '''
        self.window = window
        self.game_mode = game_mode
        self.game = Game(window, width, height, self.game_mode)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle


    def calculate_fitness(self, game_scores):
        '''(PongNeatAI, genome, genome) -> Nonetype
        This function is used to calculate the fitness of each genome playing, using the number of times they have hit the ball.
        '''
        # increase the fitness of each genome by the number of times their respective paddle has hit the ball
        self.genome1.fitness += game_scores.left_hits
        self.genome2.fitness += game_scores.right_hits


    def train_ai(self, genome1, genome2, config):
        '''(PongNeatAI, genome, genome, config) -> NoneType
        This function is used to train the AI to play Pong.
        '''

        # create neural networks for both genomes
        neural_net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        neural_net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        run = True
        while run:
            # allow the user to quit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            # store the fitness scores associated with the 3 output nodes in our neural network (these are whether a paddle should stay still or move up or down)
            output1 = neural_net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            output2 = neural_net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))

            # store the choice of movement with the highest fitness (0 = stay still, 1 = move up, 2 = move down)
            movement1 = output1.index(max(output1))
            movement2 = output2.index(max(output2))

            # move the left paddle according to the output of neural_net1, as long as the paddle does not move offscreen
            if movement1 == 0:
                self.genome1.fitness -= 0.01 # discourage non-movement from the AI
            elif movement1 == 1 and self.left_paddle.y - Paddle.VEL >= 0:
                self.left_paddle.move(up=True)
            elif movement1 == 2 and self.left_paddle.y + Paddle.VEL + Paddle.HEIGHT <= self.game.height:
                self.left_paddle.move(up=False)
            # if the movement would make the paddle go offscreen, penalize the AI to discourage invalid movements
            else:
                self.genome1.fitness -= 1

            # move the right paddle according to the output of neural_net2
            if movement2 == 0:
                self.genome2.fitness -= 0.01 # discourage non-movement from the AI
            elif movement2 == 1 and self.right_paddle.y - Paddle.VEL >= 0:
                self.right_paddle.move(up=True)
            elif movement2 == 2 and self.right_paddle.y + Paddle.VEL + Paddle.HEIGHT <= self.game.height:
                self.right_paddle.move(up=False)
            # if the movement would make the paddle go offscreen, penalize the AI to discourage invalid movements
            else:
                self.genome2.fitness -= 1

            # handle the movement of the ball and redraw the window
            game_scores = self.game.handle_ball_movement()
            self.game.draw()

            # end this iteration of the algorithm if one of the paddles misses the ball or if the ball has been successfully hit over 50 times           
            if game_scores.left_score == 1 or game_scores.right_score == 1 or game_scores.left_hits > 50:
                self.calculate_fitness(game_scores)
                break

    def play_ai(self, genome, config):
        '''(PongNeatAI, genome, config) -> Nonetype
        This function is used to allow the user to play against the trained AI.
        '''
        # store the winning neural network
        neural_net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.game.FPS)
            # allow the user to quit or pause the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause(self.window)
            
            # handle the left paddle's movements based on the user's input
            keys = pygame.key.get_pressed()
            self.game.handle_left_paddle_movement(keys)

            # handle the right paddle's movements based on the movement decision made by the AI
            output = neural_net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            movement = output.index(max(output))
            self.game.handle_right_paddle_movement(keys, movement)

            # handle the ball's movements and redraw the window
            self.game.handle_ball_movement()
            self.game.draw()

            # check if the game has been won
            self.game.if_won()

import pygame

from .ball import Ball
from .paddle import Paddle

pygame.init()

class GameScores:
    '''This class is used to track the scores in a game of Pong.'''
    def __init__(self, left_score, right_score, left_hits, right_hits):
        self.left_score = left_score
        self.right_score = right_score
        self.left_hits = left_hits
        self.right_hits = right_hits

class Game:
    '''A class to represent a game of Pong.'''
    # set the winning score and maximum frames per second for a game
    WINNING_SCORE = 5
    FPS = 60

    # set RGB values for colours that will be used in the display window
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # set the fonts to be used for the game
    SCORE_FONT = pygame.font.SysFont("impact", 50)
    WIN_FONT = pygame.font.SysFont("verdana", 60)
    PLAY_AGAIN_FONT = pygame.font.SysFont("verdana", 40)
    COUNTDOWN_FONT = pygame.font.SysFont("impact", 100)

    
    def __init__(self, window, width, height, game_mode):
        '''(Game, Window, int, int, int) -> Nonetype
        This function intitializes a game of Pong, setting up the objects and
        game information depending on the game mode that was selected by the user.
        '''
        self.window = window
        self.width = width
        self.height = height
        self.game_mode = game_mode

        # set the initial paddle positions to the centre of the y-axis, with a padding of 10 pixels on either side of the screen
        # and the ball in the centre of the screen
        self.left_paddle = Paddle(10, self.height//2 - Paddle.HEIGHT//2, Paddle.WIDTH, Paddle.HEIGHT)
        self.right_paddle = Paddle(self.width - 10 - Paddle.WIDTH, self.height//2 - Paddle.HEIGHT//2, Paddle.WIDTH, Paddle.HEIGHT)
        self.ball = Ball(self.width // 2, self.height // 2, Ball.RADIUS)

        # set all initial scores to 0
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

        # set the controls and winning message depending on the selected game mode
        if game_mode == 2:
            self.left_ctrl_up = pygame.K_w
            self.left_ctrl_down = pygame.K_s
            self.right_ctrl_up = pygame.K_UP
            self.right_ctrl_down = pygame.K_DOWN
            self.left_win_text = "LEFT PLAYER WINS!"
            self.right_win_text = "RIGHT PLAYER WINS!"
        else:
            self.left_ctrl_up = pygame.K_UP
            self.left_ctrl_down = pygame.K_DOWN
            self.left_win_text = "YOU WON!"
            self.right_win_text = "YOU LOST!"

    def handle_left_paddle_movement(self, keys):
        '''(Game, Booleans) -> Nonetype
        This function, given the current state of all keyboard buttons, checks if the
        left paddle should be moved either up or down in the next frame.
        '''
        # move the left paddle according to the user's input
        if keys[self.left_ctrl_up] and self.left_paddle.y - Paddle.VEL >= 0:
            self.left_paddle.move(up=True)
        if keys[self.left_ctrl_down] and self.left_paddle.y + Paddle.VEL + Paddle.HEIGHT <= self.height:
            self.left_paddle.move(up=False)


    def handle_right_paddle_movement(self, keys, movement=0):
        '''(Game, Booleans, int) -> Nonetype
        This function checks if the right paddle should be moved either up or down.
        This is achieved differently in each game mode.
        In a basic one-player game, the right paddle tracks the y-coordinate of the ball at all times, with a buffer of 20 pixels.
        In a two-player game, the right paddle is moved according to the second player's input.
        In a one-player game against the AI, the right paddle moves according to the movement decision of the AI at each frame.
        '''
        # In a basic one-player game, the right paddle moves depending on the current y-coordinate of the ball
        if self.game_mode == 1:
            # if the middle of the paddle is currently more than 20 pixels below the y-coordinate of the ball, move up 
            if (self.right_paddle.y + self.right_paddle.height/2 - 20 > self.ball.y) and self.right_paddle.y >= 0:
                self.right_paddle.move(up=True)
            # if the middle of the paddle is currently more than 20 pixels above the y-coordinate of the ball, move down
            elif (self.right_paddle.y + self.right_paddle.height/2 + 20 < self.ball.y) and self.right_paddle.y + self.right_paddle.height <= self.height:
                self.right_paddle.move(up=False)
        
        # In a two-player game, the right paddle is moved according to the user's input 
        elif self.game_mode == 2:
            if keys[self.right_ctrl_up] and self.right_paddle.y - Paddle.VEL >= 0:
                self.right_paddle.move(up=True)
            if keys[self.right_ctrl_down] and self.right_paddle.y + Paddle.VEL + Paddle.HEIGHT <= self.height:
                self.right_paddle.move(up=False)

        # In a one-player game against the AI, the right paddle is moved depending on the movement decision made by the AI
        elif self.game_mode == 3:
            if movement == 0:
                pass
            elif movement == 1:
                self.right_paddle.move(up=True)
            else:
                self.right_paddle.move(up=False)


    def handle_ball_movement(self):
        '''(Game) -> Nonetype
        This function handles the movements of the ball and resets the ball and scores if necessary.'''
        # move the ball and handle any collisions
        self.ball.move()
        self.handle_collision()

        # if the left paddle fails to return the ball, increase the right-player's score,
        # reset the number of hits of each paddle and reset the ball
        if self.ball.x < 0:
            self.right_score += 1
            self.ball.reset()
        # if the right paddle fails to return the ball, increase the left-player's score,
        # reset the number of hits of each paddle and reset the ball
        elif self.ball.x > self.width:
            self.left_score += 1
            self.ball.reset()

        # get and return the current scores of the game
        game_scores = GameScores(self.left_score, self.right_score, self.left_hits, self.right_hits)
        return game_scores


    def handle_collision(self):
        '''(Game) -> Nonetype
        This function handles all of the ball's collisions within the game,
        with the ceiling and floor of the window, as well as with each paddle
        and tracks the number of times that each paddle has hit the ball.
        '''
        # if the edge of the ball hits the bottom of the screen, reverse the vertical direction
        if self.ball.y + Ball.RADIUS >= self.height:
            self.ball.y_vel *= -1
        # if the edge of the ball hits the top of the screen, reverse the vertical direction
        elif self.ball.y - Ball.RADIUS <= 0:
            self.ball.y_vel *= -1

        # check if the ball is moving left
        # if so, check if the y-coordinate of the ball falls within the range of the length of the left paddle
        # next check if the left edge of the ball touches the right edge of the left paddle
        # if these conditions are met, then the ball has made contact with the left paddle, so we
        # change the direction of the ball along the x-axis, to be moving rightward
        if self.ball.x_vel < 0:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + Paddle.HEIGHT:
                if self.ball.x - Ball.RADIUS <= self.left_paddle.x + Paddle.WIDTH:
                    self.ball.x_vel *= -1
                    # calculate the current y-coordinate of the middle of the left paddle
                    middle_y = self.left_paddle.y + Paddle.HEIGHT / 2
                    # calculate the difference between the y-coordinates of the middle of the left paddle to the middle of the ball
                    difference_in_y = middle_y - self.ball.y
                    # calculate the reduction factor given the maximum displacement and maximum velocity
                    reduction_factor = (Paddle.HEIGHT / 2) / Ball.MAX_VEL
                    # calculate the angle at which the ball will be sent back
                    y_vel = difference_in_y / reduction_factor
                    # reverse the direction of the ball at the calculated angle
                    self.ball.y_vel = -1 * y_vel
                    # increment the number of times the left paddle has hit the ball
                    self.left_hits += 1

        # if the ball is moving right, check if the y-coordinate of the ball falls within the range of the length of the right paddle
        # next check if the right edge of the ball touches the left edge of the right paddle
        # if so, then the ball has made contact with the right paddle and so we change the direction of the ball along the x-axis, to be moving leftward
        else:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + Paddle.HEIGHT:
                if self.ball.x + Ball.RADIUS >= self.right_paddle.x:
                    self.ball.x_vel *= -1
                    # calculate the current y-coordinate of the middle of the left paddle
                    middle_y = self.right_paddle.y + Paddle.HEIGHT / 2
                    # calculate the difference between the y-coordinates of the middle of the left paddle to the middle of the ball
                    difference_in_y = middle_y - self.ball.y
                    # calculate the reduction factor given the maximum displacement and maximum velocity                
                    reduction_factor = (Paddle.HEIGHT / 2) / Ball.MAX_VEL
                    # calculate the angle at which the ball will be sent back
                    y_vel = difference_in_y / reduction_factor
                    # reverse the direction of the ball at the calculated angle
                    self.ball.y_vel = -1 * y_vel
                    # increment the number of times the right paddle has hit the ball
                    self.right_hits += 1


    def draw(self):
        '''(Game) -> Nonetype
        This function updates the pygame window, drawing the paddles, ball and scores.
        '''
        # fill the window with black, acts as the background colour
        self.window.fill(self.BLACK)

        # if the AI is being trained, display the total number of times the ball has been hit
        if self.game_mode == 0:
            # the current number of times the ball has been hit is drawn
            hits_text = self.SCORE_FONT.render(f"{self.left_hits + self.right_hits}", 1, self.WHITE)
            self.window.blit(hits_text, (self.width//2 - hits_text.get_width()//2, 10))
        # otherwise the current scores of each player is drawn in the centre of their respective side
        else:
            left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, self.WHITE)
            right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, self.WHITE)
            self.window.blit(left_score_text, (self.width//4 - left_score_text.get_width()//2, 20))
            self.window.blit(right_score_text, (self.width * (3/4) - left_score_text.get_width()//2, 20))

        # each paddle is drawn
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        # draws a dashed line in the centre of the window
        for i in range(10, self.height, self.height//20):
            # if i is an even number, skip this iteration, don't draw rectangle
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.window, self.WHITE, (self.width//2 - 5, i, 10, self.height//20))

        # ball is drawn
        self.ball.draw(self.window)

        # update the display, applies all of the drawing
        pygame.display.update()


    def countdown(self):
        '''(Game) -> Nonetype
        This function is used to display a countdown before starting a game so that the player(s) can prepare.
        '''
        for i in range(3, -1, -1):
            self.window.fill(self.BLACK)
            if i == 0:
                text = self.COUNTDOWN_FONT.render("START!", 1, self.WHITE)
            else:
                text = self.COUNTDOWN_FONT.render(f"{i}", 1, self.WHITE)
            self.window.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)

    def if_won(self):
        '''(Game) -> Nonetype
        This function checks if the game has been won, displays the appropriate winning message and resets the game.'''
        # check if either player has reached the set winning score and set the winning text accordingly
        won = False
        if self.left_score >= self.WINNING_SCORE:
            won = True
            win_text = self.left_win_text
        elif self.right_score >= self.WINNING_SCORE:
            won = True
            win_text = self.right_win_text

        # if the game has been won, redraw the window to update the score and output the winning message
        # the game then pauses for 5 seconds and restarts from the beginning
        if won:
            self.window.fill(self.BLACK)
            left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, self.WHITE)
            right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, self.WHITE)
            text = self.WIN_FONT.render(win_text, 1, self.WHITE)
            play_again_text = self.PLAY_AGAIN_FONT.render("Play Again? [Y/N]", 1, self.WHITE)
            self.window.blit(left_score_text, (self.width//4 - left_score_text.get_width()//2, 20))
            self.window.blit(right_score_text, (self.width * (3/4) - left_score_text.get_width()//2, 20))
            self.window.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
            self.window.blit(play_again_text, (self.width//2 - play_again_text.get_width()//2, self.height//2 - play_again_text.get_height()//2 + 160))
            pygame.display.update()

            run = True
            while run:
                for event in pygame.event.get():
                    # if the user closes the window, quit the game
                    if event.type == pygame.QUIT:
                        run = False
                        quit()
                    # otherwise, reset the game or quit depending on the user's input
                    elif event.type == pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_y]:
                            run = False
                        elif keys[pygame.K_n]:
                            quit()
            self.countdown()
            self.reset()


    def reset(self):
        '''(Game) -> Nonetype
        This function resets all objects and scores in the game.
        '''
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0


    def play_game(self):
        '''(Game) -> Nonetype
        This function acts as the main loop of the game, handling all inputs and calculations at every frame.
        '''
        run = True
        clock = pygame.time.Clock()

        # Main loop, constantly running and handles everything relating to the game (paddles, ball, collisions, etc.)
        while run:
            # ensure the game will not run at more than 60 frames per second
            clock.tick(self.FPS)

            # the window is redrawn every single frame
            self.draw()
            
            for event in pygame.event.get():
                # if the user closes the window, quit the game by stopping the main loop
                if event.type == pygame.QUIT:
                    run = False
                    quit()

            # store the current state of all keyboard buttons and handle any paddle movements
            keys = pygame.key.get_pressed()
            self.handle_left_paddle_movement(keys)
            self.handle_right_paddle_movement(keys)

            # handle the movement of the ball
            self.handle_ball_movement()

            # check if the game has been won
            self.if_won()

        pygame.quit()

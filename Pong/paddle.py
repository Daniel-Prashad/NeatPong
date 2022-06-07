import pygame

class Paddle:
    '''A class to represent a paddle.'''
    # set the colour of the paddles as white, width to 20, height to 100 and velocity to 4
    COLOUR = (255, 255, 255)
    WIDTH = 20
    HEIGHT = 100
    VEL = 4


    def __init__(self, x, y, width, height):
        '''(Paddle, int, int, int, int, Boolean) -> Nonetype
        This function initializes a Paddle with a starting x-coordinate & y-coordinate
        and a constant width & height.
        '''
        self.x = self.original_x = x    # also stores the original x-coordinate, used to reset a paddle after a game is completed
        self.y = self.original_y = y    # also stores the original y-coordinate, used to reset a paddle after a game is completed
        self.width = width
        self.height = height


    def draw(self, win):
        ''' (Paddle, Window) -> Nonetype
        This function draws a Paddle on the window.
        '''
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))


    def move(self, up=True):
        '''(Paddle, Boolean) -> Nonetype
        This function updates the y-coordinate of the paddle to be drawn in the next frame.
        '''
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL


    def reset(self):
        '''(Paddle) -> Nonetype
        This function resets the x and y-coordinates to their original values so that the paddle
        will be redrawn in its starting position, used to restart a game after one is completed.
        '''
        self.x = self.original_x
        self.y = self.original_y
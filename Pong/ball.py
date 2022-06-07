import pygame
import math
import random

class Ball:
    ''' A class to represent the ball.'''

    # set the colour of the ball to white, max velocity to 5 and radius to 7
    COLOUR = (255, 255, 255)
    MAX_VEL = 5
    RADIUS = 7

    def __init__(self, x, y, radius):
        '''(Ball, int, int, int) -> Nonetype
        This function initializes the ball with a starting x-coordinate, y-coordinate,
        x-velocity and y-velocity, and constant radius. The ball is intially set to travel
        in a horizontal line from the centre of the window towards the right side with an
        initial x-velocity equal to the set maximum velocity.
        '''
        self.x = self.original_x = x    # also stores the original x-coordinate, used to reset the ball after a game is completed
        self.y = self.original_y = y    # also stores the original y-coordinate, used to reset the ball after a game is completed
        self.radius = radius

        # the ball is initially set to randomly move left or right at a randomly generated acute angle
        direction = 1 if random.random() < 0.5 else -1
        angle = self.get_angle(-30, 30, [0])
        self.x_vel = direction * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL


    def get_angle(self, min_angle, max_angle, excluded):
        '''(Ball, int, int, [int]) -> int
        This function generates and returns a random angle between min_angle and max_angle,
        excluding those in excluded to be used for ball movement upon initialization or after the ball is reset.
        '''
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle


    def draw(self, win):
        '''(Ball, Window) -> Nonetype
        This function draws the ball on the window.
        '''
        pygame.draw.circle(win, self.COLOUR, (int(self.x), int(self.y)), self.radius)


    def move(self):
        '''(Ball) -> Nonetype
        This function updates the x- and y-coordinates of the ball according to the respective velocities.
        '''
        self.x += self.x_vel
        self.y += self.y_vel


    def reset(self):
        '''(Ball) -> Nonetype
        This function, called after a point is scored, resets the ball to its starting position.
        The ball is then set to travel at a random acute angle from the centre of the window towards
        the side of the player that scored, allowing the other player to recover.
        '''
        self.x = self.original_x
        self.y = self.original_y
        angle = self.get_angle(-30, 30, [0])
        self.x_vel *= -1
        self.y_vel = math.sin(angle) * self.MAX_VEL
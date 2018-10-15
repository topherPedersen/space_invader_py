import random
import arcade
import os

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
SPRITE_SCALING_INVADER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
MOVEMENT_SPEED = 5 # Used With Keyboard
MOVEMENT_MULTIPLIER = 5 # Used With Joystick
DEAD_ZONE = 0.05 # Joystick Related Constant (See Arcade Documentation Regarding Joysticks)
LAZER_SPEED = 7
DEATH_RAY_SPEED = 4

class Lazer(arcade.Sprite):
    def update(self):
        self.center_y += LAZER_SPEED

class DeathRay(arcade.Sprite):
    def update(self):
        self.center_y -= DEATH_RAY_SPEED

class Invader(arcade.Sprite):
    def __init__(self, imageFilenameA, imageFilenameB):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        self.texture_left = arcade.load_texture(imageFilenameA, scale=0.975)
        self.texture_right = arcade.load_texture(imageFilenameB, scale=0.975)

        # By default, face right.
        self.texture = self.texture_left

        # current direction (facing either "left" or "right")
        self.facing = "left"
    '''
    def update(self):
        # update stuf here...
    '''


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True, resizable=True)

        # Add Joystick
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion
        else:
            print("There are no Joysticks")
            self.joystick = None

        # Set Background Color
        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.defender_list = None
        self.invader_list = None
        self.lazer_list = None
        self.death_ray_list = None
        self.shield_list = None

        # Set up the player info
        self.defender_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Debugging Variable
        self.iteration = 0

        # Create Game State Variables
        self.invaderDirection = "left"
        self.bottom_invader_y_position = 99999999

        # Get Full Screen Width & Height
        self.FULL_SCREEN_WIDTH, self.FULL_SCREEN_HEIGHT = self.get_size()
        self.CENTER_X =  self.FULL_SCREEN_WIDTH / 2
        self.CENTER_Y =  self.FULL_SCREEN_HEIGHT / 2
        self.LEFT_BOUNDARY_X = self.CENTER_X - (self.CENTER_X * 0.5)
        self.RIGHT_BOUNDARY_X = self.CENTER_X + (self.CENTER_X * 0.5)

        self.leftButtonDown = False
        self.rightButtonDown = False

        self.invader_speed = 1
        self.invader_advancements = 0

    def setup(self):
        # Create Sprite Lists
        self.defender_list = arcade.SpriteList()
        self.invader_list = arcade.SpriteList()
        self.lazer_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList()
        self.death_ray_list = arcade.SpriteList()

        # Create Defender
        self.defender_sprite = arcade.Sprite("Defender.png", SPRITE_SCALING_PLAYER) # Instantiate
        self.defender_sprite.center_x = self.FULL_SCREEN_WIDTH / 2 # Position
        self.defender_sprite.center_y = self.FULL_SCREEN_HEIGHT * 0.25 # Position
        self.defender_list.append(self.defender_sprite) # Add Defender to Defender List

        # Create Shields
        for i in range(3):
            # Instantiate Shield
            shield = arcade.Sprite("Shield.png", SPRITE_SCALING_PLAYER)
            # Shield Invader
            if i == 0:
                shield.center_x = (self.FULL_SCREEN_WIDTH * 0.5) * 0.67
            elif i == 1:
                shield.center_x = self.FULL_SCREEN_WIDTH * 0.5
            elif i == 2:
                shield.center_x = (self.FULL_SCREEN_WIDTH * 0.5) * 1.33
            shield.center_y = self.FULL_SCREEN_HEIGHT * 0.334
            # Add Shield to Shield List
            self.shield_list.append(shield)

        # Create Invaders
        for i in range(36):
            # Set X & Y Positions For Top Row of Invaders
            if i == 0:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            elif i == 1:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            elif i == 2:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            elif i == 3:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            elif i == 4:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            elif i == 5:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow6A.png"
                imageFilenameB = "InvaderRow6B.png"
            # Set X & Y Positions For 2nd Row of Invaders
            elif i == 6:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            elif i == 7:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            elif i == 8:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            elif i == 9:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            elif i == 10:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            elif i == 11:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow5A.png"
                imageFilenameB = "InvaderRow5B.png"
            # Set X & Y Positions For 3rd Row of Invaders
            elif i == 12:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            elif i == 13:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            elif i == 14:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            elif i == 15:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            elif i == 16:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            elif i == 17:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow4A.png"
                imageFilenameB = "InvaderRow4B.png"
            # Set X & Y Positions For 4th Row of Invaders
            elif i == 18:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            elif i == 19:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            elif i == 20:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            elif i == 21:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            elif i == 22:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            elif i == 23:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.6
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow3A.png"
                imageFilenameB = "InvaderRow3B.png"
            # Set X & Y Positions For 5th Row of Invaders
            elif i == 24:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            elif i == 25:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            elif i == 26:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            elif i == 27:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            elif i == 28:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            elif i == 29:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow2A.png"
                imageFilenameB = "InvaderRow2B.png"
            # Set X & Y Positions For Bottom Row of Invaders
            elif i == 30:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"
            elif i == 31:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"
            elif i == 32:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"
            elif i == 33:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"
            elif i == 34:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"
            elif i == 35:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.5
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
                imageFilenameA = "InvaderRow1A.png"
                imageFilenameB = "InvaderRow1B.png"

            # Instantiate Invader
            invader = Invader(imageFilenameA, imageFilenameB)
            # Position Invader
            invader.center_x = top_row_invader_x_position
            invader.center_y = top_row_invader_y_position
            # Add Invader to Invader List
            self.invader_list.append(invader)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.defender_list.draw()
        self.invader_list.draw()
        self.lazer_list.draw()
        self.shield_list.draw()
        self.death_ray_list.draw()

    def update(self, delta_time):
        # Determine Whether the Shields Should Be removed depending on the y-coordinates
        # of the lowest invader.
        if len(self.shield_list) >= 1:
            shield_coordinates = self.shield_list[0].get_position()
            shield_ycor = shield_coordinates[1]
            if self.bottom_invader_y_position < shield_ycor + 100:
                while len(self.shield_list) >= 1:
                    self.shield_list[0].kill()

        # Determine How Fast to Move Invaders Depending on
        # How Far They Have Advanced Down the Screen
        
        if self.invader_advancements <= 2:
            self.invader_speed = 1
        elif self.invader_advancements == 3 or self.invader_advancements == 4 or self.invader_advancements == 5:
            self.invader_speed = 2
        elif self.invader_advancements == 6 or self.invader_advancements == 7:
            self.invader_speed = 3
        else:
            self.invader_speed = 4
        
        # self.invader_speed = 4

        # Count Number of Main Game-Loop Iterations
        if self.invader_speed == 1:
            if self.iteration < 1200:
                self.iteration = self.iteration + 1
            else:
                self.iteration = 1 # Reset Number Every 333000 Iterations (prevents number from getting too large)

            # Prevent Defender From Moving Off Screen or "Out of Bounds"
            defenderPosition = self.defender_sprite.get_position()
            if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
                self.defender_sprite.change_x = 0
            elif self.rightButtonDown == True and defenderPosition[0] > self.RIGHT_BOUNDARY_X:
                self.defender_sprite.change_x = 0

            # MOVE INVADERS
            # First, Move Invaders Left 10 times
            if (self.iteration == 30
                or self.iteration == 60
                or self.iteration == 90
                or self.iteration == 120
                or self.iteration == 150
                or self.iteration == 180
                or self.iteration == 210
                or self.iteration == 240
                or self.iteration == 270
                or self.iteration == 300):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    # When Invaders Reach Left Border, Move Invaders Down
                    '''
                    if self.iteration == 300: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 300:
                            self.invader_list[x].change_y = -25
            # Next, March Invaders Right 20 Times
            elif (self.iteration == 330
                or self.iteration == 360
                or self.iteration == 390
                or self.iteration == 420
                or self.iteration == 450
                or self.iteration == 480
                or self.iteration == 510
                or self.iteration == 540
                or self.iteration == 570
                or self.iteration == 600
                or self.iteration == 630
                or self.iteration == 660
                or self.iteration == 690
                or self.iteration == 720
                or self.iteration == 750
                or self.iteration == 780
                or self.iteration == 810
                or self.iteration == 840
                or self.iteration == 870
                or self.iteration == 900):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = 25
                    # When Invaders Reach Right Border, Move Invaders Down
                    '''
                    if self.iteration == 900: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 900:
                            self.invader_list[x].change_y = -25
            # Last, March Invaders Left Right 10 Times Back To The Center of the Screen
            elif (self.iteration == 930
                or self.iteration == 960
                or self.iteration == 990
                or self.iteration == 1020
                or self.iteration == 1050
                or self.iteration == 1080
                or self.iteration == 1110
                or self.iteration == 1140
                or self.iteration == 1170
                or self.iteration == 1200):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    if self.iteration == 1200: 
                        # When Invaders Reach The Middle of the Screen, Increment The Number of Invader Advancements
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
            else:
                for x in range(len(self.invader_list)):
                    self.invader_list[x].change_x = 0
                    self.invader_list[x].change_y = 0
        elif self.invader_speed == 2:
            # Move Invaders 2x Speed
            # Count Number of Main Game-Loop Iterations
            if self.iteration < 600:
                self.iteration = self.iteration + 1
            else:
                self.iteration = 1 # Reset Number Every 333000 Iterations (prevents number from getting too large)

            # Prevent Defender From Moving Off Screen or "Out of Bounds"
            defenderPosition = self.defender_sprite.get_position()
            if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
                self.defender_sprite.change_x = 0
            elif self.rightButtonDown == True and defenderPosition[0] > self.RIGHT_BOUNDARY_X:
                self.defender_sprite.change_x = 0

            # MOVE INVADERS
            # First, Move Invaders Left 10 times
            if (self.iteration == 15
                or self.iteration == 30
                or self.iteration == 45
                or self.iteration == 60
                or self.iteration == 75
                or self.iteration == 90
                or self.iteration == 105
                or self.iteration == 120
                or self.iteration == 135
                or self.iteration == 150):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    # When Invaders Reach Left Border, Move Invaders Down
                    '''
                    if self.iteration == 150:
                        self.invader_advancements = self.invader_advancements + 1
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 150:
                            self.invader_list[x].change_y = -25
            # Next, March Invaders Right 20 Times
            elif (self.iteration == 165
                or self.iteration == 180
                or self.iteration == 195
                or self.iteration == 210
                or self.iteration == 225
                or self.iteration == 240
                or self.iteration == 255
                or self.iteration == 270
                or self.iteration == 285
                or self.iteration == 300
                or self.iteration == 315
                or self.iteration == 330
                or self.iteration == 345
                or self.iteration == 360
                or self.iteration == 375
                or self.iteration == 390
                or self.iteration == 405
                or self.iteration == 420
                or self.iteration == 435
                or self.iteration == 450):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = 25
                    # When Invaders Reach Right Border, Move Invaders Down
                    '''
                    if self.iteration == 450:
                        self.invader_advancements = self.invader_advancements + 1
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 450:
                            self.invader_list[x].change_y = -25
            # Last, March Invaders Left Right 10 Times Back To The Center of the Screen
            elif (self.iteration == 465
                or self.iteration == 480
                or self.iteration == 495
                or self.iteration == 510
                or self.iteration == 525
                or self.iteration == 540
                or self.iteration == 555
                or self.iteration == 570
                or self.iteration == 585
                or self.iteration == 600):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    if self.iteration == 600: 
                        # When Invaders Reach The Middle of the Screen, Increment The Number of Invader Advancements
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
            else:
                for x in range(len(self.invader_list)):
                    self.invader_list[x].change_x = 0
                    self.invader_list[x].change_y = 0
        elif self.invader_speed == 3:
            # Move Invaders 6x Speed
            # Count Number of Main Game-Loop Iterations
            if self.iteration < 200:
                self.iteration = self.iteration + 1
            else:
                self.iteration = 1 # Reset Number Every 333000 Iterations (prevents number from getting too large)

            # Prevent Defender From Moving Off Screen or "Out of Bounds"
            defenderPosition = self.defender_sprite.get_position()
            if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
                self.defender_sprite.change_x = 0
            elif self.rightButtonDown == True and defenderPosition[0] > self.RIGHT_BOUNDARY_X:
                self.defender_sprite.change_x = 0

            # MOVE INVADERS
            # First, Move Invaders Left 10 times
            if (self.iteration == 5
                or self.iteration == 10
                or self.iteration == 15
                or self.iteration == 20
                or self.iteration == 25
                or self.iteration == 30
                or self.iteration == 35
                or self.iteration == 40
                or self.iteration == 45
                or self.iteration == 50):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    # When Invaders Reach Left Border, Move Invaders Down
                    '''
                    if self.iteration == 50: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 50:
                            self.invader_list[x].change_y = -25
            # Next, March Invaders Right 20 Times
            elif (self.iteration == 55
                or self.iteration == 60
                or self.iteration == 65
                or self.iteration == 70
                or self.iteration == 75
                or self.iteration == 80
                or self.iteration == 85
                or self.iteration == 90
                or self.iteration == 95
                or self.iteration == 100
                or self.iteration == 105
                or self.iteration == 110
                or self.iteration == 115
                or self.iteration == 120
                or self.iteration == 125
                or self.iteration == 130
                or self.iteration == 135
                or self.iteration == 140
                or self.iteration == 145
                or self.iteration == 150):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = 25
                    # When Invaders Reach Right Border, Move Invaders Down
                    '''
                    if self.iteration == 150: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 150:
                            self.invader_list[x].change_y = -25
            # Last, March Invaders Left Right 10 Times Back To The Center of the Screen
            elif (self.iteration == 155
                or self.iteration == 160
                or self.iteration == 165
                or self.iteration == 170
                or self.iteration == 175
                or self.iteration == 180
                or self.iteration == 185
                or self.iteration == 190
                or self.iteration == 195
                or self.iteration == 200):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -25
                    if self.iteration == 200: 
                        # When Invaders Reach The Middle of the Screen, Increment The Number of Invader Advancements
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
            else:
                for x in range(len(self.invader_list)):
                    self.invader_list[x].change_x = 0
                    self.invader_list[x].change_y = 0
            # END MOVING INVADERS 6X SPEED
        elif self.invader_speed == 4:
            # Move Invaders 50x Speed
            # Count Number of Main Game-Loop Iterations
            if self.iteration < 40:
                self.iteration = self.iteration + 1
            else:
                self.iteration = 1 # Reset Number Every 333000 Iterations (prevents number from getting too large)

            # Prevent Defender From Moving Off Screen or "Out of Bounds"
            defenderPosition = self.defender_sprite.get_position()
            if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
                self.defender_sprite.change_x = 0
            elif self.rightButtonDown == True and defenderPosition[0] > self.RIGHT_BOUNDARY_X:
                self.defender_sprite.change_x = 0

            # MOVE INVADERS
            # First, Move Invaders Left 10 times
            if (self.iteration == 2
                or self.iteration == 4
                or self.iteration == 6
                or self.iteration == 8
                or self.iteration == 10):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -50
                    # When Invaders Reach Left Border, Move Invaders Down
                    '''
                    if self.iteration == 10: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    '''
                    for x in range(len(self.invader_list)):
                        if self.iteration == 10:
                            self.invader_list[x].change_y = -25
            # Next, March Invaders Right 20 Times
            elif (self.iteration == 12
                or self.iteration == 14
                or self.iteration == 16
                or self.iteration == 18
                or self.iteration == 20
                or self.iteration == 22
                or self.iteration == 24
                or self.iteration == 26
                or self.iteration == 28
                or self.iteration == 30):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = 50
                    # When Invaders Reach Right Border, Move Invaders Down
                    if self.iteration == 30: 
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
                    for x in range(len(self.invader_list)):
                        if self.iteration == 30:
                            self.invader_list[x].change_y = -25
            # Last, March Invaders Left Right 10 Times Back To The Center of the Screen
            elif (self.iteration == 32
                or self.iteration == 34
                or self.iteration == 36
                or self.iteration == 38
                or self.iteration == 40):
                    for x in range(len(self.invader_list)):
                        # Flip Image of Invader
                        if self.invader_list[x].facing == "left":
                            self.invader_list[x].texture = self.invader_list[x].texture_right
                            self.invader_list[x].facing = "right"
                        else:
                            self.invader_list[x].texture = self.invader_list[x].texture_left
                            self.invader_list[x].facing = "left"
                        # Move Invader (Horizontally)
                        if self.invaderDirection == "left":
                            self.invader_list[x].change_x = -50
                    if self.iteration == 40: 
                        # When Invaders Reach The Middle of the Screen, Increment The Number of Invader Advancements
                        self.invader_advancements = self.invader_advancements + 1 # increment number of advancements
            else:
                for x in range(len(self.invader_list)):
                    self.invader_list[x].change_x = 0
                    self.invader_list[x].change_y = 0
            # END MOVING INVADERS 50X SPEED

        # LAZER BEAM 
        self.lazer_list.update()
        # Detect collisions between lazer beams, invaders, and shields
        for lazer in self.lazer_list:
            hit_list = arcade.check_for_collision_with_list(lazer, self.invader_list)
            # If lazer/invader collision detected, kill lazer beam, then kill invader.
            if len(hit_list) > 0:
                lazer.kill()
            for invader in hit_list:
                invader.kill()
            # If lazer/shield collision detected, kill lazer beam.
            hit_list = arcade.check_for_collision_with_list(lazer, self.shield_list)
            if len(hit_list) > 0:
                lazer.kill()
            # If lazer goes off screen, remove it.
            if lazer.bottom > self.FULL_SCREEN_HEIGHT:
                lazer.kill()

        # DEATH RAY
        self.death_ray_list.update()
        for deathray in self.death_ray_list:
            # Check this deathray to see if it hit a shield
            hit_list = arcade.check_for_collision_with_list(deathray, self.shield_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                deathray.kill()
            # If the bullet flies off-screen, remove it.
            if deathray.bottom < self.FULL_SCREEN_HEIGHT - self.FULL_SCREEN_HEIGHT:
                deathray.kill()

        # Select Nearest Invader to Fire Death Ray Beams at Defender
        if self.iteration % 5 == 0 and len(self.death_ray_list) == 0:
            # Get the x-coordinate of every invader
            x_coordinate = []
            for i in range(len(self.invader_list)):
                position = self.invader_list[i].get_position()
                x = position[0]
                x_coordinate.append(x)
            unique_x_coordinate = []
            for i in range(len(x_coordinate)):
                if len(unique_x_coordinate) == 0:
                    unique_x_coordinate.append(x_coordinate[i])
                else:
                    addCoordinate = True
                    for j in range(len(unique_x_coordinate)):
                        if x_coordinate[i] == unique_x_coordinate[j]:
                            addCoordinate = False
                    if addCoordinate == True:
                        unique_x_coordinate.append(x_coordinate[i])  
            # For Each Column (unique_x_coordinate), Find the Bottom Invader (lowest y-coordinate)
            bottom_invader_index = []
            bottom_invader_xcor = []
            bottom_invader_ycor = []
            for i in range(len(unique_x_coordinate)):
                bottom_invader_index.append(False)
                bottom_invader_xcor.append(unique_x_coordinate[i])
                bottom_invader_ycor.append(99999999)
            for i in range(len(unique_x_coordinate)):  
                for j in range(len(self.invader_list)):
                    coordinate = self.invader_list[j].get_position()
                    xcor = coordinate[0]
                    ycor = coordinate[1]
                    if xcor == unique_x_coordinate[i]:
                        isInColumnOfInterest = True
                    else:
                        isInColumnOfInterest = False
                    if isInColumnOfInterest == True:
                        if ycor < bottom_invader_ycor[i]:
                            bottom_invader_index[i] = j
                            bottom_invader_ycor[i] = ycor
            # Identify Invader With The Lowest Y Coordinate Position (not necessarily closest invader)
            # We will use this information elsewhere in the program to determine whether or not
            # to remove the shields between the invaders and the defender.
            for i in range(len(bottom_invader_ycor)):
                if bottom_invader_ycor[i] < self.bottom_invader_y_position:
                    self.bottom_invader_y_position = bottom_invader_ycor[i]
            # Identify The Bottom Invader Closest to the Defender on the X-Axis
            if len(bottom_invader_index) >= 1:
                indexOfClosestInvader = False
                xCoordinateOfClosestInvader = 99999999
                for i in range(len(bottom_invader_index)):
                    defender_coordinates = self.defender_list[0].get_position()
                    defender_xcor = defender_coordinates[0]
                    if abs(defender_xcor - bottom_invader_xcor[i]) < abs(defender_xcor - xCoordinateOfClosestInvader):
                        indexOfClosestInvader = bottom_invader_index[i]
                        xCoordinateOfClosestInvader = bottom_invader_xcor[i]
                # Determine whether a shield is in the way of the invader and the defender
                shieldBetweenInvaderAndDefender = False
                for i in range(len(self.shield_list)):
                    shield_coordinates = self.shield_list[i].get_position()
                    shield_xcor = shield_coordinates[0]
                    invader_coordinates = self.invader_list[indexOfClosestInvader].get_position()
                    invader_xcor = invader_coordinates[0]
                    if invader_xcor > shield_xcor - 40 and invader_xcor < shield_xcor + 40:
                        # Select Next Closest Invader not blocked by Shield
                        nextClosestInvaderIndex = False
                        for j in range(len(bottom_invader_index)):
                            if bottom_invader_xcor[j] == invader_xcor:
                                coinToss = random.randint(0, 1)
                                if coinToss == 0:
                                    one_or_negative_one = -1
                                else:
                                    one_or_negative_one = 1
                                indexOfClosestInvader = bottom_invader_index[j+one_or_negative_one]
                # Fire Death Ray From Closest Invader
                deathRay = DeathRay("Lazer.png", 0.975)
                selectedInvader = self.invader_list[indexOfClosestInvader]
                deathRay.center_x = selectedInvader.center_x
                deathRay.top = selectedInvader.bottom
                deathRay.change_x = -5 # Set Rise Equal To Negative Value so Lazer Beam Travels Downward
                self.death_ray_list.append(deathRay)

        # If Joystick is Available, Move Player When Joystick Moved
        # NOTICE: The code to move the player when a keyboard button
        # is pressed is contained in the on_key_press and on_key_release
        # methods, but the code to move the player when the joystick is
        # moved is contained here, in the update method.
        if self.joystick:
            joystick_input = self.joystick.x * MOVEMENT_MULTIPLIER
            # When the joystick is in the "left" position, and the player has not
            # gone out of bounds on the left side of the screen, move defender left.
            if joystick_input < 0 and defenderPosition[0] > self.LEFT_BOUNDARY_X:
                # Set a "dead zone" to prevent drive from a centered joystick
                if abs(joystick_input) < DEAD_ZONE:
                    self.defender_sprite.change_x = 0
                else:
                    self.defender_sprite.change_x = joystick_input
            # When the joystick is in the "right" position, and the player has not
            # gone out of bounds on the right side of the screen, move defender right.
            elif joystick_input > 0 and defenderPosition[0] < self.RIGHT_BOUNDARY_X:
                # Set a "dead zone" to prevent drive from a centered joystick
                if abs(joystick_input) < DEAD_ZONE:
                    self.defender_sprite.change_x = 0
                else:
                    self.defender_sprite.change_x = joystick_input
            # Else, stop the defender so that he does not go off the screen
            else:
                self.defender_sprite.change_x = 0

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.defender_list.update()
        self.invader_list.update()

    def on_key_press(self, key, key_modifiers):
        # EXIT FULL SCREEN WHEN ESCAPE KEY IS PRESSED
        if key == arcade.key.ESCAPE:
            self.is_full_screen = False
            self.set_fullscreen(self.is_full_screen)
            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        # MOVE DEFENDER WHEN LEFT KEY IS PRESSED
        elif key == arcade.key.LEFT:
            self.defender_sprite.change_x = -MOVEMENT_SPEED
            self.leftButtonDown = True
        # MOVE DEFENDER WHEN RIGHT KEY IS PRESSED
        elif key == arcade.key.RIGHT:
            self.defender_sprite.change_x = MOVEMENT_SPEED
            self.rightButtonDown = True
        elif key == arcade.key.SPACE:
            # If there are no other lazer beams currently on screen, then fire.
            if len(self.lazer_list) == 0:
                # Instantiate Lazer
                lazer = Lazer("Lazer.png", 0.975)
                # Position Lazer Beam
                lazer.center_x = self.defender_sprite.center_x
                lazer.bottom = self.defender_sprite.top
                # Add Lazer Beam to lazer_list
                self.lazer_list.append(lazer)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            if self.rightButtonDown == False:
                self.defender_sprite.change_x = 0
            self.leftButtonDown = False
        elif key == arcade.key.RIGHT:
            if self.leftButtonDown == False:
                self.defender_sprite.change_x = 0
            self.rightButtonDown = False

    def on_joybutton_press(self, joystick, button):
        # If there are no other lazer beams currently on screen, then fire.
        if len(self.lazer_list) == 0:
            # Instantiate Lazer
            lazer = Lazer("Lazer.png", 0.975)
            # Position Lazer Beam
            lazer.center_x = self.defender_sprite.center_x
            lazer.bottom = self.defender_sprite.top
            # Add Lazer Beam to lazer_list
            self.lazer_list.append(lazer)



    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y))


def main():
    """ Main method """
    game = MyGame()
    game.setup()
    arcade.run()

# RUN GAME
main()

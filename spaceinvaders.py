import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
SPRITE_SCALING_INVADER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
MOVEMENT_SPEED = 5 # Used With Keyboard
MOVEMENT_MULTIPLIER = 5 # Used With Joystick
DEAD_ZONE = 0.05 # Joystick Related Constant (See Arcade Documentation Regarding Joysticks)

class Invader(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        self.texture_left = arcade.load_texture("Invader.png", scale=0.975)
        self.texture_right = arcade.load_texture("Invader.png", mirrored=True, scale=0.975)

        # By default, face right.
        self.texture = self.texture_right

        # current direction (facing either "left" or "right")
        self.facing = "left"
    '''
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.texture_left
        if self.change_x > 0:
            self.texture = self.texture_right

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
    '''


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

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

        # Set up the player info
        self.defender_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Debugging Variable
        self.iteration = 0

        # Get Full Screen Width & Height
        self.FULL_SCREEN_WIDTH, self.FULL_SCREEN_HEIGHT = self.get_size()
        self.CENTER_X =  self.FULL_SCREEN_WIDTH / 2
        self.CENTER_Y =  self.FULL_SCREEN_HEIGHT / 2
        self.LEFT_BOUNDARY_X = self.CENTER_X - (self.CENTER_X * 0.5)
        self.RIGHT_BOUNDARY_X = self.CENTER_X + (self.CENTER_X * 0.5)

        self.leftButtonDown = False
        self.rightButtonDown = False

    def setup(self):
        # Create Sprite Lists
        self.defender_list = arcade.SpriteList()
        self.invader_list = arcade.SpriteList()

        # Create Defender
        self.defender_sprite = arcade.Sprite("Defender.png", SPRITE_SCALING_PLAYER) # Instantiate
        self.defender_sprite.center_x = self.FULL_SCREEN_WIDTH / 2 # Position
        self.defender_sprite.center_y = self.FULL_SCREEN_HEIGHT * 0.20 # Position
        self.defender_list.append(self.defender_sprite) # Add Defender to Defender List


        # Create Invaders
        for i in range(36):
            # Set X & Y Positions For Top Row of Invaders
            if i == 0:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 1:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 2:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 3:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 4:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 5:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.80
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
            # Set X & Y Positions For 2nd Row of Invaders
            elif i == 6:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 7:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 8:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 9:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 10:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 11:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.75
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
            # Set X & Y Positions For 3rd Row of Invaders
            elif i == 12:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 13:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 14:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 15:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 16:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 17:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.7
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
            # Set X & Y Positions For 4th Row of Invaders
            elif i == 18:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 19:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 20:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 21:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 22:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 23:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.65
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
            # Set X & Y Positions For 5th Row of Invaders
            elif i == 24:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 25:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 26:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 27:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 28:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 29:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.60
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667
            # Set X & Y Positions For Bottom Row of Invaders
            elif i == 30:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.333
            elif i == 31:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.400
            elif i == 32:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.466
            elif i == 33:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.533
            elif i == 34:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.599
            elif i == 35:
                top_row_invader_y_position = self.FULL_SCREEN_HEIGHT * 0.55
                top_row_invader_x_position = self.FULL_SCREEN_WIDTH * 0.667

            # Instantiate Invader
            invader = Invader()
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

    def update(self, delta_time):
        # Count Number of Main Game-Loop Iterations
        if self.iteration < 90:
            self.iteration = self.iteration + 1
        else: 
            self.iteration = 1 # Reset Number Every 333000 Iterations (prevents number from getting too large)

        # Prevent Defender From Moving Off Screen or "Out of Bounds"
        defenderPosition = self.defender_sprite.get_position()
        if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
            self.defender_sprite.change_x = 0
        elif self.rightButtonDown == True and defenderPosition[0] > self.RIGHT_BOUNDARY_X:
            self.defender_sprite.change_x = 0

        # Move Invaders Every 333 Iterations of the Main Game Loop 
        if self.iteration == 30 or self.iteration == 60 or self.iteration == 90:
            for x in range(36):
                if self.invader_list[x].facing == "left":
                    self.invader_list[x].texture = self.invader_list[x].texture_right
                    self.invader_list[x].facing = "right"
                else:
                    self.invader_list[x].texture = self.invader_list[x].texture_left
                    self.invader_list[x].facing = "left"

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
        print("Button {} down".format(button))

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

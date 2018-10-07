import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
SPRITE_SCALING_INVADER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__(fullscreen=True, resizable=True)
        
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

        # Get Full Screen Width & Height
        self.FULL_SCREEN_WIDTH, self.FULL_SCREEN_HEIGHT = self.get_size()
        self.CENTER_X =  self.FULL_SCREEN_WIDTH / 2
        self.CENTER_Y =  self.FULL_SCREEN_HEIGHT / 2
        self.LEFT_BOUNDARY_X = self.CENTER_X - (self.CENTER_X * 0.5)
        self.RIGHT_BOUNDARY_X = self.CENTER_X + (self.CENTER_X * 0.5)

        self.leftButtonDown = False
        self.rightButtonDown = False

    def setup(self):
        # Create your sprites and sprite lists here
        self.defender_list = arcade.SpriteList()
        self.invader_list = arcade.SpriteList()

        # Create the coins
        for i in range(13):

            # Create the coin instance
            # Coin image from kenney.nl
            invader = arcade.Sprite("Invader.png", SPRITE_SCALING_INVADER)

            # Position the coin
            invader.center_x = random.randrange(self.FULL_SCREEN_WIDTH)
            invader.center_y = random.randrange(self.FULL_SCREEN_HEIGHT)

            # Add the coin to the lists
            self.invader_list.append(invader)

        # Set up the defender
        self.defender_sprite = arcade.Sprite("Defender.png", SPRITE_SCALING_PLAYER)
        self.defender_sprite.center_x = self.FULL_SCREEN_WIDTH / 2
        self.defender_sprite.center_y = self.FULL_SCREEN_HEIGHT / 2
        self.defender_list.append(self.defender_sprite)

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
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.defender_list.update()
        self.invader_list.update()

        # Prevent Defender From Moving Off Screen or "Out of Bounds"
        defenderPosition = self.defender_sprite.get_position()
        if self.leftButtonDown == True and defenderPosition[0] < self.LEFT_BOUNDARY_X:
            self.defender_sprite.change_x = 0

        if self.rightButtonDown == True and defenderPosition[1] > self.RIGHT_BOUNDARY_X:
            self.defender_sprite.change_x = 0

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
            print("LEFT KEY PRESSED!")
        # MOVE DEFENDER WHEN RIGHT KEY IS PRESSED
        elif key == arcade.key.RIGHT:
            self.defender_sprite.change_x = MOVEMENT_SPEED
            self.rightButtonDown = True
            print("RIGHT KEY PRESSED!")

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

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

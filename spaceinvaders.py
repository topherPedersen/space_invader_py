"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.975 # NOTE: Set Slightly Below 1.0 to Prevent Unwanted Side Effects
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

        # Center ViewPort in Full Screen Mode
        # This will get the size of the window, and set the viewport to match.
        # So if the window is 1000x1000, then so will our viewport. If
        # you want something different, then use those coordinates instead.
        '''
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        arcade.set_background_color(arcade.color.BLACK)
        '''

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.defender_list = None

        # Set up the player info
        self.defender_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Get Full Screen Width & Height
        self.FULL_SCREEN_WIDTH, self.FULL_SCREEN_HEIGHT = self.get_size()

    def setup(self):
        # Create your sprites and sprite lists here
        self.defender_list = arcade.SpriteList()

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

    def update(self, delta_time):
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.defender_list.update()

    def on_key_press(self, key, key_modifiers):
        # EXIT FULL SCREEN WHEN ESCAPE KEY IS PRESSED
        if key == arcade.key.ESCAPE:
            self.is_full_screen = False
            self.set_fullscreen(self.is_full_screen)
            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        # MOVE DEFENDER WHEN UP KEY IS PRESSED
        elif key == arcade.key.UP:
            self.defender_sprite.change_y = MOVEMENT_SPEED
        # MOVE DEFENDER WHEN DOWN KEY IS PRESSED
        elif key == arcade.key.DOWN:
            self.defender_sprite.change_y = -MOVEMENT_SPEED
        # MOVE DEFENDER WHEN LEFT KEY IS PRESSED
        elif key == arcade.key.LEFT:
            self.defender_sprite.change_x = -MOVEMENT_SPEED
        # MOVE DEFENDER WHEN RIGHT KEY IS PRESSED
        elif key == arcade.key.RIGHT:
            self.defender_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.defender_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.defender_sprite.change_x = 0

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

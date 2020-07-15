from kivy.app import App
from kivy.clock import Clock
from game import SpaceGame
from kivy.uix.button import Button

class SpaceApp(App):
    def build(self):
        game = SpaceGame()
        startgame = Button(
                font_size = (game.height / 20),
                width = (game.width / 2),
                height = (game.height / 2),
                center_x = (game.width / 3.3),
                top = (game.height / 2),
                text = str(game.message),
                background_color = (0, 0, 0, 0))

        startgame.bind(on_press=self.callback)

        return game

    def callback(self, event):
        game.start()


if __name__ == '__main__':
    SpaceApp().run()

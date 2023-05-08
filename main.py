from kivy.app import App
from game import SpaceGame

class SpaceApp(App):
    def build(self):
        game = SpaceGame()
        return game

if __name__ == '__main__':
    SpaceApp().run()

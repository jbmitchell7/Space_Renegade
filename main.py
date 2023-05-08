from kivy.app import App
from kivy.clock import Clock
from game import SpaceGame

class SpaceApp(App):
    def build(self):
        game = SpaceGame()
        return game

if __name__ == '__main__':
    SpaceApp().run()

from kivy.app import App
from kivy.clock import Clock
from game import SpaceGame

class SpaceApp(App):
    def build(self):
        game = SpaceGame()
        game.start()
        game.message = ""
        return game

if __name__ == '__main__':
    SpaceApp().run()


# self.sm = SmartStartMenu()
#        self.sm.buildUp()
#        def check_button(obj):
#        #check to see which button was pressed
#            if self.sm.buttonText == 'start':
#            #remove menu
#               self.parent.remove_widget(self.sm)
#               #start the game
#               print ' we should start the game now'
#               Clock.unschedule(self.app.update)
#               Clock.schedule_interval(self.app.update, 1.0/60.0)
#               try:
#                   self.parent.remove_widget(self.aboutText)
#               except:
#                   pass
#            if self.sm.buttonText == 'about':
#               self.aboutText = Label(text = 'Flappy Ship is made by Molecular Flow Games \n Check out: https://kivyspacegame.wordpress.com')
#               self.aboutText.pos = (Window.width*0.45,Window.height*0.35)
#               self.parent.add_widget(self.aboutText)
#         #bind a callback function that repsonds to event 'on_button_release' by calling function check_button
#         self.sm.bind(on_button_release = check_button)
#         #setup listeners for smartstartmenu
#         self.parent.add_widget(self.sm)
#         self.parent.add_widget(self.app) #use this hierarchy to make it easy to deal w/buttons
#         return self.parent

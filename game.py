from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from random import randint
from components.ship import SpaceShip
from components.asteroid import SpaceAsteroid
from components.laser import SpaceLaser
from components.alien import SpaceAlien


class SpaceGame(Widget):
    ship = ObjectProperty(None)
    asteroid = ObjectProperty(None)
    laser = ObjectProperty(None)
    alien = ObjectProperty(None)
    message = StringProperty("")
    score = NumericProperty(0)
    laser_list = []
    asteroid_list = []
    alien_list = []

    #Generates asteroids
    def add_asteroid(self, dt):
        new_asteroid = SpaceAsteroid()
        new_asteroid.x = randint(self.width / 20, 4 * self.width / 5)
        new_asteroid.y = self.height
        new_asteroid.velocity_y = -2
        new_asteroid.velocity_x = 0
        self.asteroid_list.append(new_asteroid)
        self.add_widget(new_asteroid)

    #Generates aliens
    def add_alien(self, dt):
        new_alien = SpaceAlien()
        new_alien.x = randint(self.width / 20, 4 * self.width / 5)
        new_alien.y = self.height
        new_alien.velocity_y = -1
        new_alien.velocity_x = 2
        self.alien_list.append(new_alien)
        self.add_widget(new_alien)

    #Generates lasers
    def add_laser(self):
        new_laser = SpaceLaser()
        new_laser.x = self.ship.x + self.ship.width / 2
        new_laser.y = self.ship.y
        new_laser.velocity_y = 5
        new_laser.velocity_x = 0
        self.laser_list.append(new_laser)
        self.add_widget(new_laser)

    #Game Loop
    def update(self, dt):
        self.ship.move()

        #Collision Handler for hitting edge
        if (self.ship.right <= 30) or (self.ship.right > self.width):
            self.ship.velocity_x = 0

        for alien in self.alien_list:
            alien.move()
            #stops everything on collision
            if alien.collide_widget(self.ship):
                self.game_over()
                print ("alien collision")
            #removes widget when off screen
            if alien.y < 0:
                self.alien_list.remove(alien)
                self.remove_widget(alien)
            #collision handler for aliens on edge
            if (alien.x <= 50) or (alien.x >= self.width - 50):
                alien.velocity_x = alien.velocity_x * -1

        #iterates through each current asteroid
        for a in self.asteroid_list:
            a.move()
            #stops everything on collision
            if a.collide_widget(self.ship):
                self.game_over()
                print ("asteroid collision")
            #removes widget when off screen
            if a.y < 0:
                self.asteroid_list.remove(a)
                self.remove_widget(a)

        #iterates through each current laser
        for l in self.laser_list:
            l.move()
            #checks if laser has missed and is now off screen
            if l.y > self.height:
                self.laser_list.remove(l)
                self.remove_widget(l)

            for a in self.asteroid_list:
                #checks laser-asteroid collisions
                if l.collide_widget(a):
                    self.laser_list.remove(l)
                    self.remove_widget(l)

            for v in self.alien_list:
                #checks laser alien collisions
                if l.collide_widget(v):
                    self.score += 1
                    self.laser_list.remove(l)
                    self.alien_list.remove(v)
                    self.remove_widget(v)
                    self.remove_widget(l)

    #handler for touch instances
    def on_touch_down(self, touch):
        if touch.x < self.width / 3:
            self.ship.velocity = Vector (-3, 0)
        elif touch.x > (self.width * 2) / 3:
            self.ship.velocity = Vector (3, 0)
        elif touch.x >= self.width / 3 and touch.x <= (self.width*2) / 3:
            self.add_laser()

    #game over procedure
    def game_over(self):
        print ("Game Over")
        self.message = "TOUCH ANYWHERE TO START"
        for x in self.asteroid_list:
            self.remove_widget(x)

        for n in self.alien_list:
            self.remove_widget(n)

        self.asteroidList = []
        self.alien_list = []
        self.laser_list = []
        self.ship.xpos = self.width / 2
        self.ship.ypos = self.height / 2
        self.score = 0
        Clock.unschedule(self.add_asteroid)
        Clock.unschedule(self.add_alien)
        Clock.unschedule(self.update)

    #starts game-- will eventually be game menu
    def start(self):
        self.message = "TOUCH ANYWHERE TO START"
        Clock.schedule_interval(self.add_alien, 5)
        Clock.schedule_interval(self.add_asteroid, 3)
        Clock.schedule_interval(self.update, 1.0/60.0)

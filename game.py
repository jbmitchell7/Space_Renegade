from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from components.ship import SpaceShip
from components.asteroid import SpaceAsteroid
from components.laser import SpaceLaser
from components.alien import SpaceAlien


class SpaceGame(Widget):
    in_menu = True
    ship = SpaceShip()
    message = StringProperty("TOUCH ANYWHERE TO START")
    score = NumericProperty(0)
    laser_list = []
    asteroid_list = []
    alien_list = []

    #starts game-- will eventually be game menu
    def start(self):
        print ('Game Started')
        self.message = ""
        Clock.schedule_interval(self.add_alien, 5)
        Clock.schedule_interval(self.add_asteroid, 3)
        Clock.schedule_interval(self.update, 1.0/60.0)

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
                print ("alien collision")
                self.game_over()
                return
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
                print ("asteroid collision")
                self.game_over()
                return
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

            for alien in self.alien_list:
                #checks laser alien collisions
                if l.collide_widget(alien):
                    self.score += 1
                    self.laser_list.remove(l)
                    self.alien_list.remove(alien)
                    self.remove_widget(alien)
                    self.remove_widget(l)

    #game over procedure
    def game_over(self):
        print ("Game Over")
        Clock.unschedule(self.add_asteroid)
        Clock.unschedule(self.add_alien)
        Clock.unschedule(self.update)
        for a in self.asteroid_list:
            self.remove_widget(a)

        for alien in self.alien_list:
            self.remove_widget(alien)

        self.asteroid_list = []
        self.alien_list = []
        self.laser_list = []
        self.score = 0
        self.message = "TOUCH ANYWHERE TO START"
        self.in_menu = True

    #handler for touch instances
    def on_touch_down(self, touch):
        if self.in_menu:
            self.in_menu = False
            self.start()
        elif touch.x < self.width / 3:
            self.ship.velocity = Vector (-3, 0)
        elif touch.x > (self.width * 2) / 3:
            self.ship.velocity = Vector (3, 0)
        elif touch.x >= self.width / 3 and touch.x <= (self.width*2) / 3:
            self.add_laser()

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

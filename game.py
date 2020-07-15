from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from ship import SpaceShip
from asteroid import SpaceAsteroid
from random import randint
from laser import SpaceLaser
from alien import SpaceAlien


class SpaceGame(Widget):
    ship = ObjectProperty(None)
    asteroid = ObjectProperty(None)
    laser = ObjectProperty(None)
    alien = ObjectProperty(None)
    message = StringProperty("TOUCH HERE TO START")
    score = NumericProperty(0)
    laser_list = []
    asteroid_list = []
    alien_list = []

    #Generates asteroids
    def add_asteroid(self, dt):
        tmp_asteroid = SpaceAsteroid()
        tmp_asteroid.x = randint(self.width / 20, 4 * self.width / 5)
        tmp_asteroid.y = self.height
        tmp_asteroid.velocity_y = -2
        tmp_asteroid.velocity_x = 0
        self.asteroid_list.append(tmp_asteroid)
        self.add_widget(tmp_asteroid)

    #Generates aliens
    def add_alien(self, dt):
        tmp_alien = SpaceAlien()
        tmp_alien.x = randint(self.width / 20, 4 * self.width / 5)
        tmp_alien.y = self.height
        tmp_alien.velocity_y = -1
        tmp_alien.velocity_x = 2
        self.alien_list.append(tmp_alien)
        self.add_widget(tmp_alien)

    #Generates lasers
    def add_laser(self):
        tmp_laser = SpaceLaser()
        tmp_laser.x = self.ship.x + self.ship.width / 2
        tmp_laser.y = self.ship.y
        tmp_laser.velocity_y = 5
        tmp_laser.velocity_x = 0
        self.laser_list.append(tmp_laser)
        self.add_widget(tmp_laser)

    #Game Loop
    def update(self, dt):
        self.ship.move()

        #Collision Handler for hitting edge
        if (self.ship.right <= 30) or (self.ship.right > self.width):
            self.ship.velocity_x = 0

        #collision handler for aliens on edge
        for u in self.alien_list:
            if (u.x <= 50) or (u.x >= self.width - 50):
                u.velocity_x = u.velocity_x * -1

        #iterates through each current asteroid
        for t in self.asteroid_list:
            t.move()
            #stops everything on collision
            if t.collide_widget(self.ship):
                self.game_over()
                print ("asteroid collision")
            #removes widget when off screen
            if t.y < 0:
                self.remove_widget(t)

        for z in self.alien_list:
            z.move()
            #stops everything on collision
            if z.collide_widget(self.ship):
                self.game_over()
                print ("alien collision")
            #removes widget when off screen
            if z.y < 0:
                self.remove_widget(t)

        #iterates through each current laser
        for l in self.laser_list:
            l.move()
            for a in self.asteroid_list:
                #checks laser-asteroid collisions
                if l.collide_widget(a):
                    l.y = 0
                    self.remove_widget(l)

            for v in self.alien_list:
                #checks laser alien collisions
                if l.collide_widget(v):
                    self.score += 1
                    self.remove_widget(v)
                    self.remove_widget(l)
                    v.y = self.height
                    v.velocity_y = 0
                    l.y = 0


        #sets current list of lasers on screen
        tmp_laserlist = self.laser_list
        tmp_laserlist[:] = [x for x in tmp_laserlist if (x.y > -100)]
        self.laser_list = tmp_laserlist

        #sets current list of asteroid on screen
        tmp_asteroidlist = self.asteroid_list
        tmp_asteroidlist[:] = [x for x in tmp_asteroidlist if (x.y > -100)]
        self.asteroid_list = tmp_asteroidlist

        #sets current list of aliens on screen
        tmp_alienlist = self.alien_list
        tmp_alienlist[:] = [x for x in tmp_alienlist if (x.y > -100)]
        self.alien_list = tmp_alienlist

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
        self.message = "TOUCH HERE TO START"
        for x in self.asteroid_list:
            self.remove_widget(x)

        for n in self.alien_list:
            self.remove_widget(n)

        self.asteroidList = []
        self.alien_list = []
        self.laser_list = []
        self.ship.xpos = self.width / 2
        self.ship.ypos = self. height / 2
        self.score = 0
        Clock.unschedule(self.add_asteroid)
        Clock.unschedule(self.add_alien)
        Clock.unschedule(self.update)

    #starts game-- will eventually be game menu
    def start(self):
        self.message = ""
        Clock.schedule_interval(self.add_alien, 5)
        Clock.schedule_interval(self.add_asteroid, 3)
        Clock.schedule_interval(self.update, 1.0/60.0)

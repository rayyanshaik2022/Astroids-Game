from pygame.math import Vector2 as Vector
import math
import random
import pygame
from settings import *

class Game():

    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    THRUST = "thrust"
    SHOOT = "shoot"
    IDLE = "idle"

    def __init__(self, rocket, asteroid_timer : int, max_asteroids : int):
        
        self.tick = 0

        self.rocket = rocket
        self.asteroid_spawn_timer = asteroid_timer * 60
        self.asteroid_spawn_tick = 0
        self.max_asteroids = max_asteroids
        self.asteroids = []

    def controller(self, action):
        if action == Game.IDLE:
            pass
        if action == Game.TURN_RIGHT:
            self.rocket.direction += math.pi/Rocket.ROTATION_RATE
        elif action == Game.TURN_LEFT:
            self.rocket.direction -= math.pi/Rocket.ROTATION_RATE
        if action == Game.THRUST:
            self.rocket.acceleration = Rocket.ACCELERATION
        else:
            self.rocket.acceleration = 0
        if action == Game.SHOOT:
            if self.rocket.shoot_countdown < 0 and len(self.rocket.bullets) < Rocket.MAX_BULLETS:
                self.rocket.shoot_countdown = Rocket.SHOOTER_DELAY
                self.rocket.bullets.append(
                    Bullet([self.rocket.pos.x, self.rocket.pos.y], self.rocket.direction)
                )
    
    def update(self):
        self.tick += 1

        self.update_rockets()
        self.update_astroids()
        self.update_bullets()

    def update_collisions(self):

        effects = {'particles':[]}

        # rocket collisions
        rocket = self.rocket
        for asteroid in self.asteroids:
            if math.hypot(rocket.pos.x-asteroid.pos.x, rocket.pos.y-asteroid.pos.y) < asteroid.size + Rocket.RADIUS*0.8:
                
                if not rocket.dead:
                    rocket.dead = self.tick

                self.asteroids.remove(asteroid)
                continue
        # bullet collisions
        for bullet in rocket.bullets:
            for asteroid in self.asteroids:
                if math.hypot(bullet.pos.x-asteroid.pos.x, bullet.pos.y-asteroid.pos.y) < asteroid.size + bullet.SIZE:
                     
                    # This should kill the bullet
                    bullet.timer = 999

                    # Split the asteroid
                    if asteroid.size > 2*Asteroid.SIZE_RANGE[0]:
                        a = Asteroid([asteroid.pos.x, asteroid.pos.y], asteroid.size//2, len(asteroid.polygon)-1, int(asteroid.speed*0.9))
                        b = Asteroid([asteroid.pos.x, asteroid.pos.y], asteroid.size//2, len(asteroid.polygon)-1, int(asteroid.speed*0.9))

                        # Want the direction to be somewhat perpendicular to the bullet's
                        direction = bullet.direction + math.pi/2
                        a.direction = direction
                        b.direction = -direction

                        if a.speed < 0.3:
                            a.speed = random.random() + 0.3
                        if b.speed < 0.3:
                            b.speed = random.random() + 0.3

                        self.asteroids.append(a)
                        self.asteroids.append(b)

                        effects['particles'].append([asteroid.pos.x, asteroid.pos.y])

                    # Add score for rocket
                    difference = (Asteroid.SIZE_RANGE[1] - Asteroid.SIZE_RANGE[0]) // 3
                    if asteroid.size < Asteroid.SIZE_RANGE[0] + difference:
                        rocket.score += 100
                    elif asteroid.size < Asteroid.SIZE_RANGE[0] + 2*difference:
                        rocket.score += 50
                    else:
                        rocket.score += 20
                        

                    # This should kill the asteroid
                    self.asteroids.remove(asteroid)

                    continue
        
        # Returns drawing sequences such as particles
        return effects

    def update_astroids(self):

        self.asteroid_spawn_tick += 1

        # Spawn new asteroids
        SPAWN_RAD = WIDTH//2
        if self.asteroid_spawn_tick > self.asteroid_spawn_timer and len(self.asteroids) < self.max_asteroids:
            spawn_angle = random.random()*2 * math.pi*2
            self.asteroids.append(
                # make it so that they spawn properly in a circlurar area and have a target that a is apoint on a smaller circle somewhere      
                Asteroid(
                    (SPAWN_RAD*math.cos(spawn_angle)+WIDTH//2,SPAWN_RAD*math.sin(spawn_angle)+WIDTH//2), random.randint(*Asteroid.SIZE_RANGE), random.randint(6,11),
                    random.random()*2 +1
                )
            )
            self.asteroid_spawn_tick = 0
        
        for asteroid in self.asteroids:
            asteroid.pos.x += asteroid.speed * math.cos(asteroid.direction)
            asteroid.pos.y += asteroid.speed * math.sin(asteroid.direction)

            if asteroid.pos.x < 0-asteroid.size or asteroid.pos.y-asteroid.size < 0 or \
                asteroid.pos.x >= WIDTH+asteroid.size or asteroid.pos.y >= HEIGHT+asteroid.size:

                self.asteroids.remove(asteroid)
                continue

    def update_rockets(self):

        rocket = self.rocket
            
        rocket.pos += rocket.velocity

        # Teleport across if out of bounds
        if rocket.pos.x >= WIDTH:
            rocket.pos.x = 0
        if rocket.pos.x < 0:
            rocket.pos.x = WIDTH
        if rocket.pos.y >= HEIGHT:
            rocket.pos.y = 0 
        if rocket.pos.y < 0:
            rocket.pos.y = HEIGHT

        rocket.velocity.x += rocket.acceleration * math.cos(rocket.direction)
        rocket.velocity.y += rocket.acceleration * math.sin(rocket.direction)
        
        if rocket.velocity.magnitude() > Rocket.MAX_SPEED:
            rocket.velocity.scale_to_length(Rocket.MAX_SPEED)

        rocket.shoot_countdown -= 1

    def update_bullets(self):
        rocket = self.rocket
        for bullet in rocket.bullets:

            bullet.timer += 1
            if bullet.timer > Bullet.LIFESPAN*60:
                rocket.bullets.remove(bullet)
                continue

            bullet.pos.x += bullet.speed * math.cos(bullet.direction)
            bullet.pos.y += bullet.speed * math.sin(bullet.direction)

            # Teleport across if out of bounds
            if bullet.pos.x >= WIDTH:
                bullet.pos.x = 0
            if bullet.pos.x < 0:
                bullet.pos.x = WIDTH
            if bullet.pos.y >= HEIGHT:
                bullet.pos.y = 0 
            if bullet.pos.y < 0:
                bullet.pos.y = HEIGHT

class Asteroid():

    SIZE_RANGE = (15,65)

    def __init__(self, pos, size, sides, speed, point_error=0.3):

        self.pos = Vector(*pos)
        self.speed = speed
        self.acceleration = 0
        self.direction = (random.random()*2 -1) * math.pi 

        self.size = size
        self.point_error = point_error

        self.polygon = self.generate_polygon(size, sides)
    
    def generate_polygon(self, size, n):

        points = []
        
        current_rotation = 0

        for i in range(n):
            angle = current_rotation + (random.random()*2-1)*self.point_error
            points.append( [self.size * math.cos(angle), self.size * math.sin(angle)] )
            current_rotation += 2*math.pi/n
        
        return points

    def current_polygon(self):

        points = []

        for p in self.polygon:
            new_p = [p[0]*math.cos(self.direction) - p[1]*math.sin(self.direction), p[0]*math.sin(self.direction)+p[1]*math.cos(self.direction)]
            new_p[0] += self.pos.x; new_p[1] += self.pos.y
            points.append(new_p)
        
        return points
    
    def draw(self, screen):

        pygame.gfxdraw.aapolygon(screen, self.current_polygon(), COLORS['white'])
        
class Rocket():

    MAX_SPEED = 4
    ACCELERATION = 0.15

    RADIUS = 25
    ANGLE_A = 2.2
    ANGLE_B = 2.5
    ROTATION_RATE = 50

    SHOOTER_DELAY = 10
    MAX_BULLETS = 8

    def __init__(self, pos : tuple):

        self.pos = Vector(*pos)
        self.velocity = Vector(0,0)
        self.acceleration = 0
        self.direction = math.pi

        self.dead = False
        self.score = 0

        self.bullets = []
        self.shoot_countdown = Rocket.SHOOTER_DELAY
    
    def calculate_polygon(self):

        point1 = [0,Rocket.RADIUS]

        point2 = [Rocket.RADIUS*math.cos(Rocket.ANGLE_A), Rocket.RADIUS*math.sin(-Rocket.ANGLE_B)]

        point3 = [0, -Rocket.RADIUS/4]

        point4 = [-Rocket.RADIUS*math.cos(Rocket.ANGLE_A), Rocket.RADIUS*math.sin(-Rocket.ANGLE_B)]

        points = [point1, point2, point3, point4]
        translated_points = []


        for p in points:
            a = [p[0]*math.cos(self.direction-math.pi/2) - p[1]*math.sin(self.direction-math.pi/2), p[0]*math.sin(self.direction-math.pi/2)+p[1]*math.cos(self.direction-math.pi/2)]
            a[0] += self.pos.x; a[1] += self.pos.y
            translated_points.append(a)

        return translated_points
    
    def draw(self, screen):
        pygame.draw.polygon(screen, COLORS['background'], self.calculate_polygon())
        pygame.gfxdraw.aapolygon(screen, self.calculate_polygon(), COLORS['white'])

    # Draw method

class Bullet():

    SPEED = 12
    SIZE = 3
    LIFESPAN = 2 # in seconds

    def __init__(self, pos, direction):

        self.pos = Vector(*pos)
        self.speed = Bullet.SPEED
        self.direction = direction

        self.size = Bullet.SIZE
        self.timer = 0

    def draw(self, screen):
        
        pygame.gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), self.size, COLORS['white'])
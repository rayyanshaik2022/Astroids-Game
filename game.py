from pygame.math import Vector2 as Vector
import math
import random
import pygame
from settings import *
from shapely.geometry import Polygon, LineString

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

        rocket_poly = Polygon(rocket.calculate_polygon())
        rocket_view_lines = [LineString([p1, p2]) for p1, p2 in rocket.calculate_vision()]
        vision_intersections = [[] for i in range(Rocket.VISION_LINES)]

        for asteroid in self.asteroids:      
            asteroid_poly = Polygon(asteroid.current_polygon())

            if rocket_poly.intersects(asteroid_poly):
                if not rocket.dead:
                    rocket.dead = self.tick
                rocket.lives_used += 1

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
                    if not rocket.dead:
                        if asteroid.size < Asteroid.SIZE_RANGE[0] + difference:
                            rocket.score += 100
                        elif asteroid.size < Asteroid.SIZE_RANGE[0] + 2*difference:
                            rocket.score += 50
                        else:
                            rocket.score += 20
                        

                    # This should kill the asteroid
                    self.asteroids.remove(asteroid)

                    continue
        
        
        # Calculate intersections with lines and asteroids
        for asteroid in self.asteroids:
            asteroid_poly = Polygon(asteroid.current_polygon())
        
            for i, line in enumerate(rocket_view_lines):
                    try:
                        intersection = line.intersection(asteroid_poly)
                    except:
                        # Exception occurs if the generated polygon is invalid (very rare)
                        intersection = False
                    if intersection:
                        vision_intersections[i].append(intersection.coords[0])
        
          
        # sort all intersections
        #vision_intersections = sorted(vision_intersections, key= lambda: )
        cx, cy = rocket.pos.x, rocket.pos.y
        [v_line.sort(reverse=False, key=lambda x: math.hypot(cx-x[0], cy-x[1])) for v_line in vision_intersections]    
        rocket.vision_intersections = vision_intersections

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

            if asteroid.pos.x < 0-asteroid.size or asteroid.pos.y+asteroid.size < 0 or \
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
        
        rocket.distance_covered += rocket.velocity.magnitude()

        rocket.shoot_countdown -= 1

        rocket.time_alive += 1
        if rocket.acceleration != 0:
            rocket.thrust_time += 1

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
    # Should be ~8 for the actual game
    MAX_BULLETS = 0

    VISION_DISTANCE = 200
    VISION_LINES = 16

    def __init__(self, pos : tuple):

        self.pos = Vector(*pos)
        self.velocity = Vector(0,0)
        self.acceleration = 0
        self.direction = math.pi

        self.dead = False
        self.lives_used = 0
        self.score = 0

        self.vision_intersections = [[] for i in range(Rocket.VISION_LINES)]

        self.bullets = []
        self.shoot_countdown = Rocket.SHOOTER_DELAY
        self.distance_covered = 0
        self.thrust_time = 0
        self.time_alive = 0
    
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
    
    def closest_obstacles(self, obstacles):

        return sorted(obstacles, key=lambda x: math.hypot(self.pos.x-x.pos.x, self.pos.y-x.pos.y))

    def calculate_vision(self):

        center = self.pos
        direction = self.direction

        total_lines = Rocket.VISION_LINES
        lines = []

        for i in range(total_lines):
            p1 = [center.x, center.y]
            angle = direction + 2*math.pi * (i+1)/total_lines
            p2 = [center.x + math.cos(angle)*Rocket.VISION_DISTANCE, center.y + math.sin(angle)*Rocket.VISION_DISTANCE]
            lines.append([p1, p2])
        
        return lines
        
    def draw(self, screen):
        # Draw lines
        for i, p in enumerate(self.calculate_vision()):
            p1, p2 = p
            if self.vision_intersections[i] == []:
                x1, y1 = int(p1[0]), int(p1[1])
                x2, y2 = int(p2[0]), int(p2[1])
                pygame.gfxdraw.line(screen, x1, y1, x2, y2, COLORS['white'])

        # Draw intersection lines
        i_lines = self.vision_intersections
        for line in i_lines:
            if len(line) > 0:
                x, y = line[0]
                pygame.gfxdraw.line(screen, int(self.pos.x), int(self.pos.y), int(x), int(y), Color("#FF0000"))


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
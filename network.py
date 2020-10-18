import numpy as np
from game import *
from settings import *

class Population:

    def __init__(self, pop_size, generation):

        self.pop_size = pop_size
        self.generation = generation

class Genetic:

    ACTIONS = [
        Game.TURN_RIGHT,
        Game.TURN_LEFT,
        Game.THRUST,
        Game.SHOOT,
        Game.IDLE
    ]

    def __init__(self):

        # creates a random network
        self.network = self.generate_rnetwork(28, 15, 5)
    
    def generate_rnetwork(self, input_size, hidden_size, output_size):

        # hidden_size is the number of perceptrons per layer
        # Each perceptron is a vector containing '#input_size' values

        # The +1 is for a bias weight
        hidden_layer1 = np.array([[random.uniform(-1,1) for _ in range(input_size + 1)] for _ in range(hidden_size)])
        hidden_layer2 = np.array([[random.uniform(-1,1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        output_layer = np.array([[random.uniform(-1,1) for _ in range(hidden_size + 1)] for _ in range(output_size)])

        return [hidden_layer1, hidden_layer2, output_layer]

    def get_move(self, inputs):
        pass

    def get_state(self, rocket, asteroids):
        """
        This method gathers all input values and normalizes them
        """
        
        """
        Inputs:
        1. rocket.x/WIDTH
        2. rocket.y/HEIGHT
        3. rocket.acceleration / MAX ACCEL
        4. rocket.speed / MAX SPEED
        5. rocket.velocity (direction) / 2pi
        6. shooter countdown / MAX VAL
        7. rocket.direction / 2pi

        inputs from 4 closest astroids

        8. astroid.x / WIDTH
        9. astroid.y / HEIGHT
        10. astroid.speed / MAX SPEED for astroid
        11. asteroid.direction / 2pi
        12. (distance from edge to player) hypot(asteroid.pos,rocket.pos) - asteroid.size / hypot(width, height)
        
        repeat asteroid 4x

        total inputs 27. +1 for a bias.
        """
        try:
            asteroids = asteroids[:4]
        except:
            pass

        input_vector = [0 for i in range(27)]
        input_vector[0] = rocket.pos.x/WIDTH
        input_vector[1] = rocket.pos.y/HEIGHT
        input_vector[2] = rocket.acceleration/Rocket.ACCELERATION
        input_vector[3] = rocket.velocity.magnitude() / Rocket.MAX_SPEED
        input_vector[4] = math.atan2(rocket.pos.x, rocket.pos.y) / (2*math.pi)
        input_vector[5] = rocket.shoot_countdown / Rocket.SHOOTER_DELAY
        input_vector[6] = (rocket.direction%(2*math.pi)) / math.pi

        index = 7
        for i, ast in enumerate(asteroids):
            input_vector[index] = ast.pos.x / WIDTH
            input_vector[index+1] = ast.pos.y / HEIGHT
            # change asteroid max speed values to fit such
            input_vector[index+2] = ast.speed / 3
            input_vector[index+3] = (ast.direction%(2*math.pi)) / (2*math.pi)
            input_vector[index+4] = (math.hypot(rocket.pos.x-ast.pos.x, rocket.pos.y-ast.pos.y)-ast.size) / math.hypot(WIDTH, HEIGHT)

            index += 5

        input_vector = list(np.array(input_vector)) + [1]

        return np.array(input_vector)


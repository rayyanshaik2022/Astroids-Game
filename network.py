import numpy as np
from game import *
from settings import *

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

class Genetic:

    ACTIONS = [
        Game.TURN_RIGHT,
        Game.TURN_LEFT,
        Game.THRUST,
        #Game.SHOOT,
        Game.IDLE
    ]

    def __init__(self):

        # creates a random network
        
        #get_move
        #self.network = self.generate_rnetwork(27, 20, 5)

        #get_move2
        self.network = self.generate_rnetwork(7 + Rocket.VISION_LINES, 15, len(Genetic.ACTIONS))
    
    def generate_rnetwork(self, input_size, hidden_size, output_size):

        # hidden_size is the number of perceptrons per layer
        # Each perceptron is a vector containing '#input_size' values

        # The +1 is for a bias weight
        hidden_layer1 = np.array([[random.uniform(-1,1) for _ in range(input_size + 1)] for _ in range(hidden_size)])
        hidden_layer2 = np.array([[random.uniform(-1,1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        hidden_layer3 = np.array([[random.uniform(-1,1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        output_layer = np.array([[random.uniform(-1,1) for _ in range(hidden_size + 1)] for _ in range(output_size)])

        return [hidden_layer1, hidden_layer2, hidden_layer3, output_layer]

    def get_move(self, rocket, asteroids):
        
        input_vector = self.get_state2(rocket) #self.get_state(rocket, asteroids)
        hidden_layer1, hidden_layer2, hidden_layer3, output_layer = self.network

        # Forwards propagation
        # Tanh is the activation function
        # A bias is a weight that is not dependent on the input

        # Use dot product to get the output of perceptrons from the input to the hiddenlayer1
        hidden_result1 = np.array([
            math.tanh(np.dot(input_vector, hidden_layer1[i])) \
                for i in range(hidden_layer1.shape[0])] + [1]) # [1] is added as a bias

        # Use dot product to get the output of perceptrons from hiddenresult 1 to the hiddenlayer2
        hidden_result2 = np.array([
            math.tanh(np.dot(hidden_result1, hidden_layer2[i])) \
                for i in range(hidden_layer2.shape[0])] + [1]) # [1] is added as a bias
        
        # Use dot product to get the output of perceptrons from hiddenresult 1 to the hiddenlayer3
        hidden_result3 = np.array([
            math.tanh(np.dot(hidden_result2, hidden_layer3[i])) \
                for i in range(hidden_layer3.shape[0])] + [1]) # [1] is added as a bias
        
        # Use dot product to get the output of perceptrons from hiddenresult 3 to the output layer
        output_result = np.array([
            math.tanh(np.dot(hidden_result3, output_layer[i])) \
                for i in range(output_layer.shape[0])])

        max_index = np.argmax(output_result)
        return Genetic.ACTIONS[max_index]

    def get_state(self, rocket, asteroids):
        """
        This method gathers all input values and normalizes them
        """

        """
        Inputs:
        1. Rocket x Position
        2. Rocket y Position
        3. Rocket Acceleration
        4. Rocket Speed
        5. Rocket Velocity (direction)
        6. Rocket shooter countdown
        7. Rocket Direction

        - Inputs from 4 closest astroids

        8. Asteroid x Position
        9. Asteroid y Position
        10. Asteroid Speed
        11. Asteroid Direction
        12. Distance from Asteroid (edge of polygon) to Rocket
        12. (distance from edge to player)
        
        repeat asteroid 4x

        total inputs 27. +1 for a bias.
        """
        try:
            asteroids = asteroids[:4]
        except:
            pass

        input_vector = [-1 for i in range(27)]
        input_vector[0] = rocket.pos.x/WIDTH
        input_vector[1] = rocket.pos.y/HEIGHT
        input_vector[2] = rocket.acceleration/Rocket.ACCELERATION
        input_vector[3] = rocket.velocity.magnitude() / Rocket.MAX_SPEED
        input_vector[4] = math.atan2(rocket.velocity.x, rocket.velocity.y) / (2*math.pi)
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

    def get_state2(self, rocket):
        """
        This method gathers all input values and normalizes them
        """

        """
        Inputs:
        1. Rocket x Position
        2. Rocket y Position
        3. Rocket Acceleration
        4. Rocket Speed
        5. Rocket Velocity (direction)
        6. Rocket shooter countdown
        7. Rocket Direction

        - Inputs from (n)) tracing lines

        8n. length of line
        """

        input_vector = [-1 for i in range(7+Rocket.VISION_LINES)]
        input_vector[0] = rocket.pos.x/WIDTH
        input_vector[1] = rocket.pos.y/HEIGHT
        input_vector[2] = rocket.acceleration/Rocket.ACCELERATION
        input_vector[3] = rocket.velocity.magnitude() / Rocket.MAX_SPEED
        input_vector[4] = math.atan2(rocket.velocity.x, rocket.velocity.y) / (2*math.pi)
        input_vector[5] = rocket.shoot_countdown / Rocket.SHOOTER_DELAY
        input_vector[6] = (rocket.direction%(2*math.pi)) / math.pi

        c = 7
        for line in rocket.vision_intersections:
            if line == []:
                input_vector[c] = 1 # max viewdistance
            else:
                length = math.hypot(rocket.pos.x-line[0][0], rocket.pos.y-line[0][1])
                input_vector[c] = length / Rocket.VISION_DISTANCE
            c += 1

        input_vector = list(np.array(input_vector)) + [1]
        return np.array(input_vector)

class Population:

    def __init__(self, pop_size, generations, lifespan, mutation_chance=0.1, mutation_rate=0.1, network_type=Genetic):

        self.pop_size = pop_size
        self.population = [network_type() for i in range(pop_size)]
        self.generations = generations
        self.current_generation = 1
        self.lifespan = lifespan * 60 # in seconds

        self.mutation_chance = mutation_chance
        self.mutation_rate = mutation_rate

        self.network_type = network_type

        self.best_by_generation = []

    def evaluate_fitness(self, rocket):

        """
        What do we want to score?
        + points from shooting asteroids
        + time alive
        + distance covered over period alive (promotes movement or high velocity?)
        """

        score = rocket.score
        time_alive = rocket.time_alive
        distance = rocket.distance_covered/(time_alive*0.002)
        time_accelerating = rocket.thrust_time
        
        return rocket.score + time_alive + time_accelerating
    
    def crossover(self, pool, total_children):
        children = []

        for i in range(total_children):
            parentA = random.choice(pool)
            parentB = random.choice(pool)

            mid = random.randint(0, len(parentA.network[0]))
            hidden_layer1 = np.array( list(parentA.network[0][:mid]) + list(parentB.network[0][mid:]) )

            mid = random.randint(0, len(parentA.network[1]))
            hidden_layer2 = np.array( list(parentA.network[1][:mid]) + list(parentB.network[1][mid:]) )

            mid = random.randint(0, len(parentA.network[1]))
            hidden_layer3 = np.array( list(parentA.network[2][:mid]) + list(parentB.network[2][mid:]) )
            
            child = self.network_type()

            child.network[0] = hidden_layer1
            child.network[1] = hidden_layer2
            child.network[2] = hidden_layer3

            children.append(child)

        return children
    
    def mutate(self, pool):

        chance = self.mutation_chance
        rate = self.mutation_rate

        # Mutation on all layers except last
        for entity in pool:
            for layer in entity.network[:1]:

                for i in range(len(layer)):
                    if random.random() < chance:
                        layer[i] += np.random.uniform(-1,1) * rate

        return pool
    
    def train_network(self, network):

        rocket_spawn = (random.randint(300,500), random.randint(300,500)) # (400,400) as center
        g = Game(Rocket(rocket_spawn), 0.2, 10)
        
        while g.tick < self.lifespan and not g.rocket.dead:
            move = (network.get_move(g.rocket, g.rocket.closest_obstacles(g.asteroids)))
            g.controller(move)
            g.update()
            g.update_collisions()

        return self.evaluate_fitness(g.rocket)
    
    def train_generation(self):
        networks = []
        for n in self.population:
            fitness = self.train_network(n)
            networks.append((n, fitness))
        
        # sort from best to worst
        sorted_generation = sorted(networks, key=lambda x: x[1])[::-1]
        top_score = sorted_generation[0][1]
        print("Best Score: ", top_score)
        self.population = [y[0] for y in sorted_generation]

        # Take top 25%
        top_25 = self.population[:len(self.population)//4]
        top_25_children = self.crossover(top_25, len(self.population)//2)
        randoms = [self.network_type() for i in  range(self.pop_size-len(top_25)-len(top_25_children))]


        # Now mutate all of these 
        a = self.mutate(top_25)
        b = self.mutate(top_25_children)
        c = self.mutate(randoms)
        self.population = a+b+c

        # Elitism: Also include the highest performing network, unmodified
        self.population.insert(0,top_25[0])
        self.population = self.population[:-1]

        # Done with 1 generation
        # Return score of the best performing network

        return top_score
    
    def train(self):
        for i in range(self.generations):
            print("Gen:",self.current_generation)
            top_score = self.train_generation()
            self.best_by_generation.append((self.population[0], top_score))
            self.current_generation += 1
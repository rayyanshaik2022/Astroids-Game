# Astroids Game & Deep Genetic Network
---
## Game Content
- Within this project, I have recreated my own version of the classic Atari game, 'Asteroids'. My version stays true to the original in terms of gameplay and aesthetics but is designed to be easily incorporated with learning agents and neural networks
- ### Key Design Features
    - **Object Orient Programming (OOP)** for all abstractable features. The rocket, asteroids, and bullets are represented through their own classes - `Rocket`, `Asteroid`, `Bullet`.
    - **Asteroid Mechanics**: I have developed my own method (as a mathematical computation) to create uniquely shaped asteroids that resemble circular objects, yet are polygons. Large asteroids also have the ability to 'split' when hit.
    - **Particle Effects**: Through the classes `Particle` and `ParticleManager`, the program controls 'individual particles' that contribute to the overall visual effect. These effects are present during rocket thrusting and asteroid splitting.
    - The game itself is not designed to run with a GUI active 100% of the time. I created the game so that it could run independently as its own environment and updates as called. However, by design, it is also easy to implement a GUI with the `Game` class (as implemented in the `GUI` class).

## Neural Network
- In order to create a playable agent for this game, I decided to develop a neural network. This neural network contains perceptrons, layers, and forwards propagation.
- ### Network Structure
    - 27 (+1 bias) input values
    - 3 Hidden layers, each with (default) 20 perceptrons
    - 1 output layer with 5 values (each representing an action)
- ### Forward Propagation
    - Used to make the prediction for the next action
    - `tanh()` used as the activation function

## Deep Genetic Algorithm

## Genetic Algorithm Optimization Observations
- ### Testing Round A
    - **Observations**: A 'lightly' trained rocket would even up turning in circles and shoot randomly. While this may have been a good solution within 20 seconds, it is not a good long term solution. To counteract this, I added bias in the fitness evaluation function to add score by how far the rocket travels. This incentivizes the rocket to apply thrust.

## Learning Resources
- The concept and code for this project was developed 100% by myself.
These are the links to resources that I used to learn about neural networks and genetic algorithms, 
as well efficiency with the numpy library for creating neural networks
- [Coding Challenge #29: Smart Rockets in p5.js](https://www.youtube.com/watch?v=bGz7mv2vD6g)
- [Snake AI | Genetic Algorithm | Python](https://www.youtube.com/watch?v=SGxVaptD9Ug&list=LL&index=1&t=746s)
- [The Number of Hidden Layers](https://www.heatonresearch.com/2017/06/01/hidden-layers.html#:~:text=The%20number%20of%20hidden%20neurons,size%20of%20the%20input%20layer.)
- [Create a Simple Neural Network in Python from Scratch](https://www.youtube.com/watch?v=kft1AJ9WVDk&t=653s)
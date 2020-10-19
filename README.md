# Astroids Game & Deep Genetic Network
---
## Game Content
- Within this project, I have recreated my own version of the classic Atari game, 'Asteroids'. My version stays true to the original in terms of gameplay and aesthetics but is designed to be easily incorporated with learning agents and neural networks
- ### Key Design Features
    - **Object Orient Programming (OOP)** for all abstractable features. The rocket, asteroids, and bullets are represented through their own classes - `Rocket`, `Asteroid`, `Bullet`.
    - **Asteroid Mechanics**: I have developed my own method (as a mathematical computation) to create uniquely shaped asteroids that resemble circular objects, yet are polygons. Large asteroids also have the ability to 'split' when hit.
    - **Particle Effects**: Through the classes `Particle` and `ParticleManager`, the program controls 'individual particles' that contribute to the overall visual effect. These effects are present during rocket thrusting and asteroid splitting.
    - The game itself is not designed to run with a GUI active 100% of the time. I created the game so that it could run independently as its own environment and updates as called. However, by design, it is also easy to implement a GUI with the `Game` class (as implemented in the `GUI` class).


## Learning Resources
- The concept and code for this project was developed 100% by myself.
These are the links to resources that I used to learn about neural networks and genetic algorithms, 
as well efficiency with the numpy library for creating neural networks
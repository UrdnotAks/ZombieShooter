# ZombieShooter
A simple zombie shooter game where the player tries to survive a zombie attack

# How To?
The player's position is fixed at the centre of the screen. The zombies are randomly spawned at different predefined spawn points and are moved towards the player.
The player turns around and shoots the zombies. If the player hits a zombie, the game is over.
The player is controlled by the mouse and LeftMouseButton is used to shoot.

# Playing the game
Download and place all the files in the same folder. Run the 'ZombieShooter.py' in any python IDE. You must have the pygame module installed for the game to work.

# Bugs
The collisions are not pixel perfect and may cause false collision registers which result in a game over.
Also the player can shoot infinite number of bullets from his handgun. It is due to the fact that the player's movement is restricted and while reloading, it puts the player in a defenseless position. So, I need to find a workaround before placing a limit on the bullets.

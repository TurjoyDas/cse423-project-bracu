# cse423-project-bracu

Galaxy Attack: Project Description

Overview:
Galaxy Attack is an engaging 2D arcade-style game developed using Python, OpenGL, and the GLUT library. The shapes are drawn using only Midpoint Line and Midpoint Circle algorithm. It immerses players in a dynamic and fast-paced space combat scenario, where they control a shooter to battle waves of enemies, dodge obstacles, and face off against a challenging boss. The game is designed to test the player’s reflexes, strategy, and accuracy while offering a nostalgic retro gaming experience. It is a 2 player game, one player will be the shooter, another player will control the enemy.

# Key Features:

Player Shooter Mechanics:

1) The player controls a shooter with directional movement (up, down, left, right) using arrow keys.

2) Players can fire bullets or activate a laser beam for advanced combat.

3) Health points are displayed, and bonuses such as health regeneration are available.

Enemy Waves:

1) Multiple enemies spawn with different shapes (Box, Circle, Triangle) and health levels.

2) Enemies move dynamically, posing increasing difficulty as the game progresses.

Boss Fight:

1) A formidable boss appears after players achieve a specific score.

2) The boss features advanced movements, multiple health levels, and a variety of attack patterns, including firing multiple bullets.

Power-Ups and Obstacles:

1) Power-ups like hearts restore the player’s health when collected.

2) Invisible mode temporarily shields the shooter from enemy attacks.

Dynamic Starfield:

1) A visually appealing starfield scrolls in the background to create a space-themed ambiance.

Collision Detection:

1) Implements precise collision logic for interactions between bullets, lasers, enemies, and the shooter.

Scoring System:

1) Players earn points for defeating enemies and surviving waves.

2) The score resets when transitioning to the boss fight, adding to the challenge.

Gameplay Controls:

Arrow Keys: Move the shooter.

Spacebar: Fire bullets.

"L" Key: Activate or deactivate the laser.

Numeric Keys (1-5): Enemy or boss-specific attack modes.

Technical Details:

Graphics Rendering: The game uses OpenGL for rendering objects, such as the shooter, enemies, bullets, and stars.

Animation: Smooth animations for shooter movements, enemy waves, and bullet trajectories.

Collision Handling: Bounding box detection for bullets and lasers ensures accurate interaction between game elements.

Custom Algorithms: Midpoint algorithms are used for drawing shapes like circles and lines to ensure smooth rendering.

# Shifting Maze

A turn-based roguelike. Escape 5 floors, but the walls move where you cannot see them,
so when you turn back the passages are different.

play it in main.py

Keys: `w a s d` move or attack, `e` class ability, `.` wait, `q` quit.

`main.py` Starts the game and picks your class. Run this one.
`game.py` One run: floors, turns, drawing, enemies and the shifting walls.
`maze.py` Makes a random maze, finds paths, checks what can be seen.
`heroes.py` The classes: Warrior (Smash), Rogue (Dash), Mage (Anchor).
`upgrades.py` The upgrades you choose from after each floor.
`enemies.py` The monsters: rat, goblin, brute.

Add a class: write a new `Hero` subclass in `heroes.py` and add it to `HEROES`.
Add an upgrade: add one `Upgrade(...)` line to `UPGRADES` in `upgrades.py`.
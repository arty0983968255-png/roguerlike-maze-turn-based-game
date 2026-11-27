"""classesn and ability."""

from maze import FLOOR, WALL
class Hero:
    name = "Hero"
    max_hp = 20
    attack = 4
    defense = 0
    view = 3
    ability_name = "Nothing"
    ability_info = ""
    ability_cooldown = 5
    def __init__(self):
        self.hp = self.max_hp
        self.x = 1
        self.y = 1
        self.cooldown = 0
        self.shift_bonus = 0
    def use_ability(self, game) -> bool:
        """Return True if the ability used up the turn."""
        game.say("You have no ability.")
        return False
class Warrior(Hero):
    name = "Warrior"
    max_hp = 30
    attack = 5
    defense = 2
    view = 3
    ability_name = "Smash"
    ability_info = "break the wall next to you, then wait 6 turns"
    ability_cooldown = 6
    def use_ability(self, game) -> bool:
        direction = game.ask_direction()
        if direction is None:
            return False
        wx, wy = self.x + direction[0], self.y + direction[1]
        inside = 0 < wx < game.width - 1 and 0 < wy < game.height - 1
        if not inside or game.grid[wy][wx] != WALL:
            game.say("There is no wall you can smash there.")
            return False
        game.grid[wy][wx] = FLOOR
        self.cooldown = self.ability_cooldown + 1
        game.say("CRASH! You smash through the wall.")
        return True
class Rogue(Hero):
    name = "Rogue"
    max_hp = 22
    attack = 4
    defense = 1
    view = 4
    ability_name = "Dash"
    ability_info = "run up to 3 tiles in one turn, then wait 5 turns"
    ability_cooldown = 5
    def use_ability(self, game) -> bool:
        direction = game.ask_direction()
        if direction is None:
            return False
        moved = 0
        for _ in range(3):
            nx, ny = self.x + direction[0], self.y + direction[1]
            if game.grid[ny][nx] == WALL or game.enemy_at(nx, ny) is not None:
                break
            self.x, self.y = nx, ny
            moved += 1
            game.pick_up()
        if moved == 0:
            game.say("Something blocks your dash.")
            return False
        self.cooldown = self.ability_cooldown + 1
        game.say(f"You dash {moved} tiles.")
        return True
class Mage(Hero):
    name = "Mage"
    max_hp = 16
    attack = 3
    defense = 0
    view = 3
    ability_name = "Anchor"
    ability_info = "the walls do not move for 5 turns, then wait 9 turns"
    ability_cooldown = 9
    def use_ability(self, game) -> bool:
        game.frozen = 5
        self.cooldown = self.ability_cooldown + 1
        game.say("You anchor the maze: the walls will not move for 5 turns.")
        return True
HEROES = {"1": Warrior, "2": Rogue, "3": Mage}
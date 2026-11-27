import os
import random
from enemies import ENEMY_TYPES, Enemy
from heroes import Hero
from maze import DIRS, FLOOR, WALL, find_path, line_clear, make_maze
from upgrades import UPGRADES
FINAL_FLOOR=5
def clear() -> None:
    os.system("cls" if os.name=="nt" else "clear")
class Game:
    def __init__(self, hero: Hero):
        self.hero = hero
        self.floor = 0
        self.log: list[str] = []
        self.quit = False
        self.start_floor()
    def start_floor(self) -> None:
        self.floor += 1
        self.width = 19 + 2 * self.floor  # always odd
        self.height = 13 + 2 * self.floor
        self.grid = make_maze(self.width, self.height)
        self.exit = (self.width - 2, self.height - 2)
        self.hero.x, self.hero.y = 1, 1
        self.memory = [[None] * self.width for _ in range(self.height)]
        self.exit_seen = False
        self.frozen = 0
        self.shift_every = max(4, 9 - self.floor) + self.hero.shift_bonus
        self.countdown = self.shift_every
        self.shift_size = max(3, self.width * self.height // 60)
        self.place_things()
        self.log = []
        self.say(f"Floor {self.floor} of {FINAL_FLOOR}: find the exit (E).")
        self.say("The walls move where you cannot see them.")
    def place_things(self) -> None:
        cells = []  # cell tiles never turn into walls
        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                far = abs(x - 1) + abs(y - 1) >= 8
                if far and (x, y) != self.exit:
                    cells.append((x, y))
        random.shuffle(cells)
        self.enemies: list[Enemy] = []
        kinds = ENEMY_TYPES[: min(3, 1 + (self.floor + 1) // 2)]
        for _ in range(2 + self.floor):
            x, y = cells.pop()
            name, symbol, hp, attack = random.choice(kinds)
            self.enemies.append(Enemy(name, symbol, hp + self.floor // 2, attack, x, y))
        self.potions = set()
        for _ in range(3):
            self.potions.add(cells.pop())
    def say(self, text: str) -> None:
        self.log.append(text)
        self.log = self.log[-5:]
    def enemy_at(self, x: int, y: int):
        for enemy in self.enemies:
            if (enemy.x, enemy.y) == (x, y):
                return enemy
        return None
    def ask_direction(self):
        text = input("Direction (w a s d)? ").strip().lower()
        return DIRS.get(text[:1])
    def visible(self) -> set:
        """The tiles the hero can see right now."""
        hero = self.hero
        seen = set()
        r = hero.view
        for y in range(hero.y - r, hero.y + r + 1):
            for x in range(hero.x - r, hero.x + r + 1):
                if not (0 <= x < self.width and 0 <= y < self.height):
                    continue
                if (x - hero.x) ** 2 + (y - hero.y) ** 2 > r * r + 1:
                    continue
                if line_clear(self.grid, hero.x, hero.y, x, y):
                    seen.add((x, y))
        return seen
    
    def draw(self) -> None:
        clear()
        hero = self.hero
        seen = self.visible()
        for x, y in seen:
            self.memory[y][x] = self.grid[y][x]  # what you last saw is what you remember
            if (x, y) == self.exit:
                self.exit_seen = True
        enemy_at = {(e.x, e.y): e.symbol for e in self.enemies}
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                spot = (x, y)
                if spot == (hero.x, hero.y):
                    row += "@"
                elif spot == self.exit and self.exit_seen:
                    row += "E"
                elif spot in seen:
                    if spot in enemy_at:
                        row += enemy_at[spot]
                    elif spot in self.potions:
                        row += "!"
                    else:
                        row += self.grid[y][x]
                elif self.memory[y][x] == WALL:
                    row += "#"  # it may have changed
                else:
                    row += " "
            print(row)
        if self.frozen > 0:
            shift_text = f"Maze anchored ({self.frozen})"
        else:
            shift_text = f"Shift in {self.countdown}"
        if hero.cooldown > 0:
            ability_text = f"{hero.ability_name}: {hero.cooldown} turns"
        else:
            ability_text = f"{hero.ability_name}: READY (e)"
        print(f"\n{hero.name}  Floor {self.floor}/{FINAL_FLOOR}  HP {hero.hp}/{hero.max_hp}"
              f"  ATK {hero.attack}  DEF {hero.defense}")
        print(f"{shift_text}   {ability_text}")
        print("@ you  E exit  ! potion  r g B enemies  # wall  . you see it now  blank = remembered/unknown")
        print()
        for line in self.log:
            print(line)

    # player's actions

    def handle(self, command: str) -> bool:
        """Do what the player typed. Return True if it used up the turn."""
        hero = self.hero
        key = command[:1]
        if key in DIRS:
            dx, dy = DIRS[key]
            nx, ny = hero.x + dx, hero.y + dy
            enemy = self.enemy_at(nx, ny)
            if enemy is not None:
                self.attack(enemy)
                return True
            if self.grid[ny][nx] == WALL:
                self.say("A wall. (That did not use a turn.)")
                return False
            hero.x, hero.y = nx, ny
            self.pick_up()
            return True
        if key == "e":
            if hero.cooldown > 0:
                self.say(f"{hero.ability_name} is not ready: {hero.cooldown} more turns.")
                return False
            return hero.use_ability(self)
        if key in (".", "x"):
            self.say("You wait.")
            return True
        if key == "q":
            self.quit = True
            return False
        self.say("Use w a s d, e, . or q.")
        return False

    def attack(self, enemy: Enemy) -> None:
        damage = self.hero.attack + random.randint(0, 1)
        enemy.hp -= damage
        if enemy.hp <= 0:
            self.enemies.remove(enemy)
            self.say(f"You hit the {enemy.name} for {damage}. It dies!")
        else:
            self.say(f"You hit the {enemy.name} for {damage}. ({enemy.hp} HP left)")

    def pick_up(self) -> None:
        spot = (self.hero.x, self.hero.y)
        if spot in self.potions:
            self.potions.remove(spot)
            healed = min(8, self.hero.max_hp - self.hero.hp)
            self.hero.hp += healed
            self.say(f"You drink a potion (+{healed} HP).")

    # what happens after player's turn

    def end_turn(self) -> None:
        hero = self.hero
        if hero.cooldown > 0:
            hero.cooldown -= 1
        self.enemy_turns()
        if self.frozen > 0:
            self.frozen -= 1
            if self.frozen == 0:
                self.say("The anchor fades.")
        else:
            self.countdown -= 1
            if self.countdown <= 0:
                self.shift_maze()
                self.countdown = self.shift_every

    def enemy_turns(self) -> None:
        hero = self.hero
        seen = self.visible()
        occupied = {(e.x, e.y) for e in self.enemies}
        for enemy in self.enemies:
            here = (enemy.x, enemy.y)
            distance = abs(enemy.x - hero.x) + abs(enemy.y - hero.y)
            if distance == 1:
                damage = max(1, enemy.attack - hero.defense)
                hero.hp -= damage
                self.say(f"The {enemy.name} hits you for {damage}.")
                continue
            step = None
            if here in seen and distance <= 8:  # it can see
                path = find_path(self.grid, here, (hero.x, hero.y), occupied - {here})
                if path:
                    step = path[0]
            elif random.random() < 0.5:  # wanders
                options = []
                for dx, dy in DIRS.values():
                    nxt = (enemy.x + dx, enemy.y + dy)
                    if self.grid[nxt[1]][nxt[0]] == FLOOR and nxt not in occupied:
                        if nxt != (hero.x, hero.y):
                            options.append(nxt)
                if options:
                    step = random.choice(options)
            if step is not None and step != (hero.x, hero.y):
                occupied.discard(here)
                enemy.x, enemy.y = step
                occupied.add(step)

    def shift_maze(self) -> None:
        """Open some walls and close some passages, but only out of the hero's sight."""
        hero = self.hero
        protected = self.visible() | {self.exit, (hero.x, hero.y)}
        protected |= {(e.x, e.y) for e in self.enemies}
        protected |= self.potions
        walls, passages = [], []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if x % 2 == y % 2 or (x, y) in protected:
                    continue  # skip cells, pillars and anything protected
                if self.grid[y][x] == WALL:
                    walls.append((x, y))
                else:
                    passages.append((x, y))
        random.shuffle(walls)
        random.shuffle(passages)
        for x, y in walls[: self.shift_size]:
            self.grid[y][x] = FLOOR
        closed = passages[: self.shift_size]
        for x, y in closed:
            self.grid[y][x] = WALL
        # the maze always solvable
        while closed and find_path(self.grid, (hero.x, hero.y), self.exit) is None:
            x, y = closed.pop()
            self.grid[y][x] = FLOOR
        self.say("Somewhere out of sight, the walls grind and shift...")

    # floors and the main loop

    def choose_upgrade(self) -> str:
        options = random.sample(UPGRADES, 3)
        print("\nChoose an upgrade:")
        for number, upgrade in enumerate(options, 1):
            print(f"  {number}. {upgrade.name}: {upgrade.text}")
        while True:
            pick = input("Pick 1-3: ").strip()
            if pick in ("1", "2", "3"):
                chosen = options[int(pick) - 1]
                chosen.apply(self.hero)
                return chosen.name

    def play(self) -> bool:
        """Play until the hero dies, quits or escapes. True means a win."""
        while True:
            self.draw()
            command = input("> ").strip().lower()
            if not self.handle(command):
                if self.quit:
                    print("You gave up.")
                    return False
                continue
            if (self.hero.x, self.hero.y) == self.exit:  # you escape before enemies act
                if self.floor == FINAL_FLOOR:
                    print("\nYou escaped the Shifting Maze! You win!")
                    return True
                print(f"\nYou reached the exit of floor {self.floor}!")
                self.hero.hp = min(self.hero.max_hp, self.hero.hp + self.hero.max_hp // 4)
                name = self.choose_upgrade()
                self.start_floor()
                self.say(f"Upgrade taken: {name}.")
                continue
            self.end_turn()
            if self.hero.hp <= 0:
                self.draw()
                print(f"\nYou died on floor {self.floor}. Game over.")
                return False
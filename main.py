"""run this file to play
Keys:  w a s d = move or attack      e = use your class ability
       . = wait a turn               q = quit
Reach the exit E on every floor. The maze only changes where you can not see, so the
map you remember gets out of date: when you turn back, the passages are different.
"""

from game import FINAL_FLOOR, Game
from heroes import HEROES, Hero
def choose_hero() -> Hero:
    print("SHIFTING MAZE")
    print(f"Escape {FINAL_FLOOR} floors. The walls move when you are not looking.\n")
    for key, kind in HEROES.items():
        print(f"{key}. {kind.name}: HP {kind.max_hp}, ATK {kind.attack}, DEF {kind.defense}, "
              f"sight {kind.view}")
        print(f"   {kind.ability_name}: {kind.ability_info}")
    while True:
        pick = input("\nPick a class (1-3): ").strip()
        if pick in HEROES:
            return HEROES[pick]()
def main() -> None:
    try:
        while True:
            Game(choose_hero()).play()
            if input("\nPlay again? (y/n) ").strip().lower() != "y":
                break
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
if __name__ == "__main__":
    main()

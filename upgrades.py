"""upgrades after each floor."""

from dataclasses import dataclass
from typing import Callable
from heroes import Hero
@dataclass
class Upgrade:
    name: str
    text: str
    apply: Callable[[Hero], None]
def more_hp(hero: Hero)->None:
    hero.max_hp+=6
    hero.hp+=6
def stronger(hero: Hero)->None:
    hero.attack+=2
def armor(hero: Hero)->None:
    hero.defense+=1
def lantern(hero: Hero)->None:
    hero.view+=1
def steady_walls(hero: Hero)->None:
    hero.shift_bonus+=2
def quick_learner(hero: Hero)->None:
    hero.ability_cooldown=max(2, hero.ability_cooldown-2)
def second_wind(hero: Hero)->None:
    hero.hp=hero.max_hp
UPGRADES=[
    Upgrade("Thick Skin", "+6 max HP", more_hp),
    Upgrade("Sharp Blade", "+2 attack", stronger),
    Upgrade("Iron Armor", "+1 defense", armor),
    Upgrade("Lantern", "+1 sight radius", lantern),
    Upgrade("Steady Walls", "the maze shifts 2 turns less often", steady_walls),
    Upgrade("Quick Learner", "ability cooldown 2 turns shorter", quick_learner),
    Upgrade("Second Wind", "heal to full HP now", second_wind),
]
from dataclasses import dataclass
@dataclass
class Enemy:
    name: str
    symbol: str
    hp: int
    attack: int
    x: int
    y: int
ENEMY_TYPES=[("rat", "r", 4, 2), ("goblin", "g", 8, 3), ("brute", "B", 13, 5)]
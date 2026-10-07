from dataclasses import dataclass
from typing import Optional


@dataclass
class EnemyState:
    # Enemy information
    health: float
    ammo: int

    # Player information
    player_detected: bool
    player_distance: float
    player_in_attack_range: bool
    line_of_sight: bool

    # Position information
    enemy_position: tuple
    player_position: Optional[tuple] = None
    last_known_player_position: Optional[tuple] = None
import math
from dataclasses import dataclass


@dataclass
class PerceptionResult:
    player_detected: bool
    player_distance: float
    player_in_attack_range: bool
    line_of_sight: bool

def calculate_distance(position1, position2):
    """
    Calculate the distance between two positions.
    """

    x1, y1 = position1
    x2, y2 = position2

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distance


def is_player_detected(
    enemy_position,
    player_position,
    detection_range
):
    """
    Check whether the player is within the enemy's detection range.
    """

    distance = calculate_distance(
        enemy_position,
        player_position
    )

    return distance <= detection_range


def is_player_in_attack_range(
    enemy_position,
    player_position,
    attack_range
):
    """
    Check whether the player is close enough to attack.
    """

    distance = calculate_distance(
        enemy_position,
        player_position
    )

    return distance <= attack_range
def perceive_enemy(
    enemy_position,
    player_position,
    detection_range,
    attack_range,
    can_see_player
):
    distance = calculate_distance(
        enemy_position,
        player_position
    )

    detected = (
        distance <= detection_range
        and can_see_player
    )

    attackable = (
        distance <= attack_range
        and can_see_player
    )

    return PerceptionResult(
        player_detected=detected,
        player_distance=distance,
        player_in_attack_range=attackable,
        line_of_sight=can_see_player
    )
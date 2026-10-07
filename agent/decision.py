from enum import Enum
from state import EnemyState

class EnemyAction(Enum):
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    SEARCH = "search"
    RETREAT = "retreat"
    
def decide_action(state: EnemyState) -> EnemyAction:

    # 1. Low health → retreat
    if state.health <= 30:
        return EnemyAction.RETREAT

   # Player is close and NPC can attack
    if (
        state.player_detected
        and state.player_in_attack_range
        and state.ammo > 0
    ):
        return EnemyAction.ATTACK

    # 3. Player detected but not close enough → chase
    if state.player_detected:
        return EnemyAction.CHASE

    # 4. Player was previously detected but is now lost → search
    if (
        not state.player_detected
        and state.last_known_player_position is not None
    ):
        return EnemyAction.SEARCH

    # 5. Nothing happening → patrol
    return EnemyAction.PATROL
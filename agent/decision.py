from enum import Enum
from agent.behaviors.patrol import patrol_behavior
from agent.behaviors.chase import chase_behavior
from agent.behaviors.attack import attack_behavior
from agent.behaviors.search import search_behavior
from agent.behaviors.retreat import retreat_behavior


class EnemyAction(Enum):
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    SEARCH = "search"
    RETREAT = "retreat"


def decide_action(state, memory):

    # 1. Low health
    if state.health <= 30:
        return retreat_behavior(
            state.enemy_position,
            state.player_position
        )

    # 2. Attack
    if (
        state.player_detected
        and state.player_in_attack_range
        and state.ammo > 0
    ):
        return attack_behavior()

    # 3. Chase
    if state.player_detected:
        return chase_behavior(
            state.player_position
        )

    # 4. Search
    if (
        memory.search_active
        and not memory.search_expired()
        and memory.last_known_player_position is not None
    ):
        return search_behavior(
            memory.last_known_player_position
        )

    # 5. Otherwise patrol
    return patrol_behavior()
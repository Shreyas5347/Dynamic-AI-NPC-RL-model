from state import EnemyState
from memory import EnemyMemory
from perception import perceive_enemy
from decision import decide_action


class EnemyAgent:

    def __init__(
        self,
        detection_range=15.0,
        attack_range=3.0
    ):
        self.detection_range = detection_range
        self.attack_range = attack_range

        self.memory = EnemyMemory()

    def update(
        self,
        enemy_position,
        player_position,
        health,
        ammo,
        can_see_player
    ):

        # 1. Perception
        perception = perceive_enemy(
            enemy_position=enemy_position,
            player_position=player_position,
            detection_range=self.detection_range,
            attack_range=self.attack_range,
            can_see_player=can_see_player
        )

        # 2. Update memory
        self.memory.update(
            player_detected=perception.player_detected,
            player_position=player_position
        )

        # 3. Create current enemy state
        state = EnemyState(
            health=health,
            ammo=ammo,
            player_detected=perception.player_detected,
            player_distance=perception.player_distance,
            player_in_attack_range=perception.player_in_attack_range,
            line_of_sight=perception.line_of_sight,
            enemy_position=enemy_position,
            player_position=(
                player_position
                if perception.player_detected
                else None
            ),
            last_known_player_position=(
                self.memory.last_known_player_position
            )
        )

        # 4. Make decision
        action = decide_action(state)

        return state, action
#enemyAgent connects Perception,Memory,Decision,Action


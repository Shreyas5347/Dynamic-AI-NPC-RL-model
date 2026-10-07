from state import EnemyState
from decision import decide_action


state = EnemyState(
    health=100,
    ammo=10,
    player_detected=True,
    player_distance=20,
    player_in_attack_range=True,
    line_of_sight=True,
    enemy_position=(5, 5),
    player_position=(10, 10),
    last_known_player_position=(10, 10)
)

action = decide_action(state)

print("Enemy decision:", action.value)
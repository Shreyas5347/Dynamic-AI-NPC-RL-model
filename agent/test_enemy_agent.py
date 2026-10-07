from agent import EnemyAgent


enemy = EnemyAgent(
    detection_range=15,
    attack_range=3
)


state, action = enemy.update(
    enemy_position=(0, 0),
    player_position=(2, 0),
    health=20,
    ammo=10,
    can_see_player=True
)

state, action = enemy.update(
    enemy_position=(5, 0),
    player_position=(10, 0),
    health=100,
    ammo=10,
    can_see_player=False
)

print("Second decision:", action.value)
print(
    "Last known position:",
    state.last_known_player_position
)

print("Player detected:", state.player_detected)
print("Player distance:", state.player_distance)
print("Enemy decision:", action.value)
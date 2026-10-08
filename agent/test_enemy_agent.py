from agent.agent import EnemyAgent


enemy = EnemyAgent(
    detection_range=15,
    attack_range=3
)


# -----------------------------------
# Situation 1: Player detected
# -----------------------------------

state, action = enemy.update(
    enemy_position=(0, 0),
    player_position=(10, 0),
    health=100,
    ammo=10,
    can_see_player=True
)

print("\nSituation 1")
print("Decision:", action["behavior"])
print("Reason:", action["reason"])


# -----------------------------------
# Situation 2: Player close
# -----------------------------------

state, action = enemy.update(
    enemy_position=(0, 0),
    player_position=(2, 0),
    health=100,
    ammo=10,
    can_see_player=True
)

print("\nSituation 2")
print("Decision:", action["behavior"])
print("Reason:", action["reason"])


# -----------------------------------
# Situation 3: Player disappears
# -----------------------------------

state, action = enemy.update(
    enemy_position=(5, 0),
    player_position=(2, 0),
    health=100,
    ammo=10,
    can_see_player=False
)

print("\nSituation 3")
print("Decision:", action["behavior"])
print("Target:", action["target"])


# -----------------------------------
# Situation 4: Low health
# -----------------------------------

state, action = enemy.update(
    enemy_position=(5, 0),
    player_position=(2, 0),
    health=20,
    ammo=10,
    can_see_player=False
)

print("\nSituation 4")
print("Decision:", action["behavior"])
print("Reason:", action["reason"])
from memory import EnemyMemory


memory = EnemyMemory()

player_position = (10, 20)


print("Initial memory:")
print(memory)


memory.update(
    player_detected=True,
    player_position=player_position
)

print("\nAfter detecting player:")
print(memory)


memory.update(
    player_detected=False,
    player_position=player_position
)

print("\nAfter losing player:")
print(memory)
from agent.perception import perceive_enemy


enemy_position = (0, 0)
player_position = (5, 0)

result = perceive_enemy(
    enemy_position=enemy_position,
    player_position=player_position,
    detection_range=10,
    attack_range=5,
    can_see_player=False
)

print("Player detected:", result.player_detected)
print("Player distance:", result.player_distance)
print("Player in attack range:", result.player_in_attack_range)
print("Line of sight:", result.line_of_sight)
def retreat_behavior(enemy_position, player_position):
    """
    Move away from the player when health is low.
    """

    return {
        "behavior": "RETREAT",
        "target": player_position,
        "reason": "Enemy health is low"
    }
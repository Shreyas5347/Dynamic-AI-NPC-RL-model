def chase_behavior(target_position):
    """
    Move toward the player's current or last known position.
    """

    return {
        "behavior": "CHASE",
        "target": target_position,
        "reason": "Player detected"
    }
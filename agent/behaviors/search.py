def search_behavior(last_known_position):
    """
    Search the last known location of the player.
    """

    return {
        "behavior": "SEARCH",
        "target": last_known_position,
        "reason": "Player was lost"
    }
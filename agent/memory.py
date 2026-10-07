from dataclasses import dataclass
from typing import Optional


@dataclass
class EnemyMemory:

    last_known_player_position: Optional[tuple] = None
    player_was_detected: bool = False

    def update(self, player_detected, player_position):

        if player_detected:
            self.last_known_player_position = player_position
            self.player_was_detected = True

        else:
            self.player_was_detected = False
    def forget(self):
        """
        Reset memory when player is completely gone for too long.
        """
        self.last_known_player_position = None
        self.player_was_detected = False
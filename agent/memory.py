from dataclasses import dataclass
from typing import Optional


@dataclass
class EnemyMemory:

    last_known_player_position: Optional[tuple] = None
    player_was_detected: bool = False

    search_active: bool = False
    search_time: float = 0.0

    def update(self, player_detected, player_position, delta_time=1.0):

        if player_detected:

            self.last_known_player_position = player_position
            self.player_was_detected = True

            # Player found again
            self.search_active = False
            self.search_time = 0.0

        else:

            # Player is currently not visible
            if self.player_was_detected:

                self.search_active = True

            self.player_was_detected = False

            # Increase search time
            if self.search_active:
                self.search_time += delta_time

    def search_expired(self, max_search_time=10.0):

        return self.search_time >= max_search_time
import gymnasium as gym
import minigrid

from minigrid.core.grid import Grid
from minigrid.core.world_object import Wall, Goal
from minigrid.core.mission import MissionSpace
from minigrid.minigrid_env import MiniGridEnv


class ObstacleEnv(MiniGridEnv):

    def __init__(self, **kwargs):

        mission_space = MissionSpace(
            mission_func=lambda: "reach the goal"
        )

        super().__init__(
            mission_space=mission_space,
            grid_size=8,
            max_steps=100,
            **kwargs
        )

    def _gen_grid(self, width, height):

        # Create empty grid
        self.grid = Grid(width, height)

        # Surround the map with walls
        self.grid.wall_rect(
            0,
            0,
            width,
            height
        )

        # ------------------------------------------
        # NPC starting position
        # ------------------------------------------

        self.agent_pos = (1, 1)
        self.agent_dir = 0

        # ------------------------------------------
        # Goal
        # ------------------------------------------

        self.put_obj(
            Goal(),
            width - 2,
            height - 2
        )

        # ------------------------------------------
        # Obstacles
        # ------------------------------------------

        obstacles = [

            # Horizontal wall
            (3, 2),
            (4, 2),
            (5, 2),

            # Vertical wall
            (5, 3),
            (5, 4),

            # Another obstacle
            (2, 5),
            (3, 5),
            (4, 5),

        ]

        for x, y in obstacles:

            self.put_obj(
                Wall(),
                x,
                y
            )

        # Mission
        self.mission = "reach the goal"
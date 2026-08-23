import random
from collections import deque

from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.grid import Grid
from minigrid.core.world_object import Wall, Goal
from minigrid.core.mission import MissionSpace


class RandomObstacleEnv(MiniGridEnv):

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

    # ==================================================
    # Generate the grid
    # ==================================================

    def _gen_grid(self, width, height):

        while True:

            # --------------------------------------------------
            # Create empty grid
            # --------------------------------------------------

            self.grid = Grid(width, height)

            # --------------------------------------------------
            # Outer walls
            # --------------------------------------------------

            self.grid.wall_rect(
                0,
                0,
                width,
                height
            )

            # --------------------------------------------------
            # NPC starting position
            # --------------------------------------------------

            self.agent_pos = (1, 1)
            self.agent_dir = 0

            # --------------------------------------------------
            # Goal position
            # --------------------------------------------------

            goal_pos = (
                width - 2,
                height - 2
            )

            self.put_obj(
                Goal(),
                goal_pos[0],
                goal_pos[1]
            )

            # --------------------------------------------------
            # Generate possible obstacle positions
            # --------------------------------------------------

            possible_positions = []

            for x in range(1, width - 1):

                for y in range(1, height - 1):

                    if (
                        (x, y) != self.agent_pos
                        and
                        (x, y) != goal_pos
                    ):

                        possible_positions.append(
                            (x, y)
                        )

            # --------------------------------------------------
            # Random number of obstacles
            # --------------------------------------------------

            obstacle_count = random.randint(
                5,
                10
            )

            obstacle_positions = random.sample(
                possible_positions,
                obstacle_count
            )

            # --------------------------------------------------
            # Place obstacles
            # --------------------------------------------------

            for x, y in obstacle_positions:

                self.put_obj(
                    Wall(),
                    x,
                    y
                )

            # --------------------------------------------------
            # Check if goal is reachable
            # --------------------------------------------------

            if self._path_exists(
                self.agent_pos,
                goal_pos,
                width,
                height
            ):

                break

            # If no path exists,
            # generate a completely new map.

        # --------------------------------------------------
        # Mission
        # --------------------------------------------------

        self.mission = "reach the goal"

    # ==================================================
    # BFS PATH CHECK
    # ==================================================
#we are using breadth-first search(bfs) to check if a path exists between the agent and the goal.
#it checks whether a path exists before npc agent getting trained which avoids impossible path 
# if a path is unreachable,a new map is generated.   
    def _path_exists(
        self,
        start,
        goal,
        width,
        height
    ):

        queue = deque()

        queue.append(start)

        visited = set()

        visited.add(start)

        # Four possible movement directions

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while queue:

            current = queue.popleft()

            # Goal reached

            if current == goal:

                return True

            x, y = current

            for dx, dy in directions:

                nx = x + dx
                ny = y + dy

                # Stay inside the map

                if not (
                    0 <= nx < width
                    and
                    0 <= ny < height
                ):
                    continue

                next_position = (
                    nx,
                    ny
                )

                # Already visited

                if next_position in visited:

                    continue

                # Check whether cell is blocked

                cell = self.grid.get(
                    nx,
                    ny
                )

                # Walls cannot be crossed

                if cell is not None:

                    if cell.type == "wall":

                        continue

                # Valid cell

                visited.add(
                    next_position
                )

                queue.append(
                    next_position
                )

        # No path found

        return False
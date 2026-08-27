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
    # GENERATE GRID
    # ==================================================

    def _gen_grid(self, width, height):

        while True:

            self.grid = Grid(
                width,
                height
            )

            # Outer walls
            self.grid.wall_rect(
                0,
                0,
                width,
                height
            )

            # Agent
            self.agent_pos = (1, 1)
            self.agent_dir = 0

            # Goal
            self.goal_pos = (
                width - 2,
                height - 2
            )

            self.put_obj(
                Goal(),
                self.goal_pos[0],
                self.goal_pos[1]
            )

            # --------------------------------------------------
            # Random obstacles
            # --------------------------------------------------

            possible_positions = []

            for x in range(
                1,
                width - 1
            ):

                for y in range(
                    1,
                    height - 1
                ):

                    position = (
                        x,
                        y
                    )

                    if (
                        position != self.agent_pos
                        and
                        position != self.goal_pos
                    ):

                        possible_positions.append(
                            position
                        )

            obstacle_count = random.randint(
                5,
                8
            )

            obstacle_positions = random.sample(
                possible_positions,
                obstacle_count
            )

            for x, y in obstacle_positions:

                self.put_obj(
                    Wall(),
                    x,
                    y
                )

            # --------------------------------------------------
            # Make sure path exists
            # --------------------------------------------------

            if self._path_exists(
                self.agent_pos,
                self.goal_pos,
                width,
                height
            ):

                break

        self.mission = "reach the goal"

        # Initial distance
        self.previous_distance = self._manhattan_distance(
            self.agent_pos,
            self.goal_pos
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):

        observation, info = super().reset(
            seed=seed,
            options=options
        )

        self.previous_distance = (
            self._manhattan_distance(
                self.agent_pos,
                self.goal_pos
            )
        )

        return observation, info

    # ==================================================
    # STEP
    # ==================================================

    def step(
        self,
        action
    ):

        # Store old position
        old_position = self.agent_pos

        # Let MiniGrid perform the action
        observation, reward, terminated, truncated, info = super().step(
            action
        )

        # --------------------------------------------------
        # Distance before/after action
        # --------------------------------------------------

        old_distance = self._manhattan_distance(
            old_position,
            self.goal_pos
        )

        new_distance = self._manhattan_distance(
            self.agent_pos,
            self.goal_pos
        )

        # --------------------------------------------------
        # Reward shaping
        # --------------------------------------------------

        # Small penalty for every action
        reward = -0.01

        # Reward for getting closer
        if new_distance < old_distance:

            reward += 0.1

        # Penalty for moving away
        elif new_distance > old_distance:

            reward -= 0.05

        # Goal reached
        if terminated:

            reward += 1.0

        return (
            observation,
            reward,
            terminated,
            truncated,
            info
        )

    # ==================================================
    # MANHATTAN DISTANCE
    # ==================================================

    def _manhattan_distance(
        self,
        position_a,
        position_b
    ):

        return (
            abs(position_a[0] - position_b[0])
            +
            abs(position_a[1] - position_b[1])
        )

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
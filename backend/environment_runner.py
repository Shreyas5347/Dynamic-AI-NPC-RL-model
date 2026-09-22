"""
EnvironmentRunner — wraps RandomObstacleEnv + NavigationActionWrapper + FlatObsWrapper + PPO
and exposes a clean synchronous API that the async WebSocket handler calls via run_in_executor.
"""

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from environments.obstacle_env import RandomObstacleEnv
from environments.navigation_wrapper import NavigationActionWrapper
from minigrid.wrappers import FlatObsWrapper
from stable_baselines3 import PPO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECKPOINTS_DIR = os.path.join(PROJECT_ROOT, "models", "checkpoints")


def get_available_checkpoints() -> list[int]:
    """Return sorted list of available checkpoint timestep numbers."""
    checkpoints = []
    if not os.path.exists(CHECKPOINTS_DIR):
        return checkpoints
    for fname in os.listdir(CHECKPOINTS_DIR):
        if fname.endswith(".zip") and fname.startswith("ppo_"):
            try:
                ts = int(fname.replace("ppo_", "").replace(".zip", ""))
                checkpoints.append(ts)
            except ValueError:
                pass
    return sorted(checkpoints)


class EnvironmentRunner:
    """
    Thread-safe (synchronous) wrapper around the RL environment + model.
    All methods are blocking — call them via asyncio.get_event_loop().run_in_executor().
    """

    def __init__(self):
        self._env = None
        self._model: Optional[PPO] = None
        self._obs = None
        self.checkpoint: Optional[int] = None

        # Per-episode state
        self.episode: int = 0
        self.episode_reward: float = 0.0
        self.episode_steps: int = 0
        self.total_steps: int = 0
        self.is_done: bool = False

        # Aggregate metrics
        self._episode_rewards: list[float] = []
        self._episode_steps_hist: list[int] = []
        self._successes: int = 0

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def load_model(self, checkpoint: int) -> None:
        path = os.path.join(CHECKPOINTS_DIR, f"ppo_{checkpoint}")
        self._model = PPO.load(path)
        self.checkpoint = checkpoint

    def create_env(self) -> None:
        if self._env is not None:
            try:
                self._env.close()
            except Exception:
                pass
        env = RandomObstacleEnv()
        env = NavigationActionWrapper(env)
        env = FlatObsWrapper(env)
        self._env = env

    def reset_stats(self) -> None:
        self.episode = 0
        self.episode_reward = 0.0
        self.episode_steps = 0
        self.total_steps = 0
        self.is_done = False
        self._episode_rewards = []
        self._episode_steps_hist = []
        self._successes = 0

    # ------------------------------------------------------------------
    # Episode management
    # ------------------------------------------------------------------

    def start_episode(self) -> dict:
        """Reset the env to a new random grid and start a new episode."""
        self.episode += 1
        self.episode_reward = 0.0
        self.episode_steps = 0
        self.is_done = False
        obs, _ = self._env.reset()
        self._obs = obs
        return self.get_state()

    def step(self) -> dict:
        """Run one environment step using the loaded model."""
        if self._obs is None or self._model is None or self._env is None:
            raise RuntimeError("Runner not fully initialized — call load_model, create_env, start_episode first.")

        action, _ = self._model.predict(self._obs, deterministic=False)
        obs, reward, terminated, truncated, _ = self._env.step(int(action))
        self._obs = obs

        reward = float(reward)
        self.episode_reward += reward
        self.episode_steps += 1
        self.total_steps += 1

        if terminated or truncated:
            self.is_done = True
            self._episode_rewards.append(self.episode_reward)
            self._episode_steps_hist.append(self.episode_steps)
            if self.episode_reward > 0:
                self._successes += 1

        return self.get_state()

    # ------------------------------------------------------------------
    # State serialization
    # ------------------------------------------------------------------

    def get_state(self) -> dict:
        raw = self._env.unwrapped  # RandomObstacleEnv

        cells = []
        for y in range(raw.height):
            for x in range(raw.width):
                cell = raw.grid.get(x, y)
                if cell is None:
                    t = "empty"
                elif cell.type == "wall":
                    t = "wall"
                elif cell.type == "goal":
                    t = "goal"
                else:
                    t = "empty"
                cells.append({"x": x, "y": y, "type": t})

        n_eps = len(self._episode_rewards)
        success_rate = (self._successes / n_eps * 100) if n_eps > 0 else 0.0
        avg_reward = sum(self._episode_rewards) / n_eps if n_eps > 0 else 0.0
        avg_steps = sum(self._episode_steps_hist) / n_eps if n_eps > 0 else 0.0

        return {
            "width": raw.width,
            "height": raw.height,
            "cells": cells,
            "agent": {
                "x": int(raw.agent_pos[0]),
                "y": int(raw.agent_pos[1]),
                "dir": int(raw.agent_dir),
            },
            "goal": {
                "x": int(raw.goal_pos[0]),
                "y": int(raw.goal_pos[1]),
            },
            "episode": self.episode,
            "step": self.episode_steps,
            "reward": round(self.episode_reward, 4),
            "is_done": self.is_done,
            "metrics": {
                "success_rate": round(success_rate, 1),
                "avg_reward": round(avg_reward, 4),
                "avg_steps": round(avg_steps, 1),
                "total_timesteps": self.checkpoint or 0,
                "total_episodes": n_eps,
                "successful_episodes": self._successes,
                # Last 100 episode rewards for the chart
                "episode_rewards": self._episode_rewards[-100:],
            },
        }

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        if self._env is not None:
            try:
                self._env.close()
            except Exception:
                pass
            self._env = None

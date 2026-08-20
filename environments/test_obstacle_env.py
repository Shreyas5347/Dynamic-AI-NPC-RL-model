import gymnasium as gym
import time
import os
import sys

# Add project root to path so environments package can be resolved
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from environments.obstacle_env import ObstacleEnv


env = ObstacleEnv(
    render_mode="human"
)

observation, info = env.reset()

print("Environment started!")

for step in range(100):

    # Random action
    action = env.action_space.sample()

    observation, reward, terminated, truncated, info = env.step(
        action
    )

    time.sleep(0.2)

    if terminated or truncated:

        print("Episode finished!")

        observation, info = env.reset()


env.close()
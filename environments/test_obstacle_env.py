import time

from environments.obstacle_env import RandomObstacleEnv


env = RandomObstacleEnv(
    render_mode="human"
)


# --------------------------------------------------
# Run multiple episodes
# --------------------------------------------------

for episode in range(5):

    observation, info = env.reset()

    print(
        f"\nEpisode {episode + 1}"
    )

    for step in range(100):

        action = env.action_space.sample()

        observation, reward, terminated, truncated, info = env.step(
            action
        )

        time.sleep(0.15)

        if terminated or truncated:

            print(
                f"Episode finished after {step + 1} steps"
            )

            break


env.close()
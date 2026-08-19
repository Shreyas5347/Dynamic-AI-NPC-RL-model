import gymnasium as gym
import minigrid
import time


# Create the MiniGrid environment
env = gym.make(
    "MiniGrid-Empty-8x8-v0",
    render_mode="human"
)

# Start a new episode
observation, info = env.reset()

print("Action Space:")
print(env.action_space)

print("\nObservation Space:")
print(env.observation_space)

print("\nStarting random actions...\n")


# Take 20 random actions
for step in range(20):

    # Choose a random action
    action = env.action_space.sample()

    # Send the action to the environment
    observation, reward, terminated, truncated, info = env.step(action)

    print(
        f"Step: {step + 1} | "
        f"Action: {action} | "
        f"Reward: {reward}"
    )

    # Give yourself time to see the movement
    time.sleep(0.3)

    # If the episode ends, start a new one
    if terminated or truncated:
        print("Episode ended. Resetting...")
        observation, info = env.reset()


# Close the environment
env.close()

print("\nMiniGrid test completed successfully!")
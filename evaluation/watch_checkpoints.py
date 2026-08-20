import gymnasium as gym
import minigrid
import pygame
import time
import os
import sys

# Add project root to path so environments package can be resolved
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from minigrid.wrappers import FlatObsWrapper
from stable_baselines3 import PPO
from environments.obstacle_env import ObstacleEnv


# ==================================================
# SETTINGS
# ==================================================

CHECKPOINT = 25000

MODEL_PATH = f"models/checkpoints/ppo_{CHECKPOINT}"

# Resolve path relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "checkpoints", f"ppo_{CHECKPOINT}")
# ==================================================
# CREATE ENVIRONMENT
# ==================================================

env = ObstacleEnv(
    render_mode="human"
)
env = FlatObsWrapper(env)


# ==================================================
# LOAD TRAINED MODEL
# ==================================================

model = PPO.load(
    MODEL_PATH,
    env=env
)


# ==================================================
# START SCREEN
# ==================================================

pygame.init()

screen = pygame.display.set_mode((600, 150))
pygame.display.set_caption(
    f"RL NPC Evaluation - {CHECKPOINT:,} Timesteps"
)

font = pygame.font.Font(None, 32)

button = pygame.Rect(
    200,
    50,
    200,
    60
)

waiting = True


print("=" * 60)
print(f"RL NPC EVALUATION - CHECKPOINT {CHECKPOINT:,}")
print("=" * 60)
print("Click START in the evaluation window.")


# ==================================================
# WAIT FOR START BUTTON
# ==================================================

while waiting:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            env.close()
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if button.collidepoint(event.pos):

                waiting = False

    screen.fill((30, 30, 30))

    pygame.draw.rect(
        screen,
        (70, 130, 200),
        button
    )

    text = font.render(
        "START",
        True,
        (255, 255, 255)
    )

    text_rect = text.get_rect(
        center=button.center
    )

    screen.blit(
        text,
        text_rect
    )

    pygame.display.flip()

    time.sleep(0.01)


# ==================================================
# CLOSE START SCREEN
# ==================================================

pygame.quit()


# ==================================================
# START MINI-GRID
# ==================================================

observation, info = env.reset()

print("\nEvaluation started!")

episode = 1


# ==================================================
# RUN TRAINED NPC
# ==================================================

MAX_EPISODES = 10
MAX_STEPS_PER_EPISODE = 500

episode = 1
total_steps = 0

observation, info = env.reset()

print("\nEvaluation started!")

while episode <= MAX_EPISODES:

    episode_steps = 0
    episode_reward = 0

    terminated = False
    truncated = False

    while not (terminated or truncated) and episode_steps < MAX_STEPS_PER_EPISODE:

        action, _states = model.predict(
            observation,
            deterministic=False
        )

        observation, reward, terminated, truncated, info = env.step(
            action
        )

        episode_steps += 1
        total_steps += 1
        episode_reward += reward

        # Show progress in terminal
        print(
            f"\rEpisode: {episode} | "
            f"Step: {episode_steps} | "
            f"Total steps: {total_steps} | "
            f"Reward: {episode_reward:.2f}",
            end=""
        )

        # Slow down NPC for recording
        time.sleep(0.15)

    print(
        f"\nEpisode {episode} finished | "
        f"Steps: {episode_steps} | "
        f"Reward: {episode_reward:.2f}"
    )

    episode += 1

    if episode <= MAX_EPISODES:
        time.sleep(1)
        observation, info = env.reset()

print(f"\nTotal evaluation steps: {total_steps}")
# ==================================================
# CLOSE
# ==================================================

env.close()

print("\nEvaluation completed!")
import os
import sys
import time

import gymnasium as gym
import minigrid
import pygame

from minigrid.wrappers import FlatObsWrapper
from stable_baselines3 import PPO


from environments.obstacle_env import RandomObstacleEnv
from environments.navigation_wrapper import NavigationActionWrapper

# ==================================================
# SETTINGS
# ==================================================

CHECKPOINT = 10000

MAX_EPISODES = 10
MAX_STEPS_PER_EPISODE = 200

SLEEP_TIME = 0.15


# ==================================================
# PROJECT PATH
# ==================================================

SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..")
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "checkpoints",
    f"ppo_{CHECKPOINT}"
)


# ==================================================
# CHECK MODEL
# ==================================================

if not os.path.exists(MODEL_PATH + ".zip"):

    print(
        f"ERROR: Model not found:\n"
        f"{MODEL_PATH}.zip"
    )

    sys.exit()


# ==================================================
# START BUTTON WINDOW
# ==================================================

pygame.init()

screen = pygame.display.set_mode(
    (600, 180)
)

pygame.display.set_caption(
    f"RL NPC Evaluation - "
    f"{CHECKPOINT:,} Timesteps"
)

font = pygame.font.Font(
    None,
    32
)

small_font = pygame.font.Font(
    None,
    24
)

button = pygame.Rect(
    200,
    70,
    200,
    60
)


# ==================================================
# WAIT FOR START
# ==================================================

waiting = True

while waiting:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and button.collidepoint(event.pos)
        ):

            waiting = False


    screen.fill(
        (30, 30, 30)
    )


    title = font.render(
        "RL NPC Evaluation",
        True,
        (255, 255, 255)
    )

    title_rect = title.get_rect(
        center=(300, 30)
    )

    screen.blit(
        title,
        title_rect
    )


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
# CLOSE START WINDOW
# ==================================================

pygame.display.quit()


# ==================================================
# CREATE MINIGRID AFTER START
# ==================================================

env = RandomObstacleEnv(
    render_mode="human"
)

env = NavigationActionWrapper(env)
env = FlatObsWrapper(env)


# ==================================================
# LOAD MODEL
# ==================================================

model = PPO.load(
    MODEL_PATH
)


# ==================================================
# START EVALUATION
# ==================================================

observation, info = env.reset()

print("\nEvaluation started!")

print(
    f"Checkpoint: {CHECKPOINT:,}"
)

print(
    f"Episodes: {MAX_EPISODES}"
)


# ==================================================
# RESULTS
# ==================================================

all_rewards = []
all_steps = []

successful_episodes = 0

total_steps = 0


# ==================================================
# RUN EPISODES
# ==================================================

for episode in range(
    1,
    MAX_EPISODES + 1
):

    episode_reward = 0
    episode_steps = 0

    terminated = False
    truncated = False


    while (
        not terminated
        and not truncated
        and episode_steps < MAX_STEPS_PER_EPISODE
    ):

        # --------------------------------------------------
        # Predict action
        # --------------------------------------------------

        action, _ = model.predict(
            observation,
            deterministic=False
        )


        # --------------------------------------------------
        # Step environment
        # --------------------------------------------------

        observation, reward, terminated, truncated, info = env.step(
            action
        )


        episode_reward += reward

        episode_steps += 1

        total_steps += 1


        # --------------------------------------------------
        # Terminal progress
        # --------------------------------------------------

        print(
            f"\rEpisode: {episode} | "
            f"Step: {episode_steps} | "
            f"Reward: {episode_reward:.2f}",
            end=""
        )


        # --------------------------------------------------
        # Slow down for recording
        # --------------------------------------------------

        time.sleep(
            SLEEP_TIME
        )


    # ==================================================
    # EPISODE RESULT
    # ==================================================

    all_rewards.append(
        episode_reward
    )

    all_steps.append(
        episode_steps
    )


    if episode_reward > 0:

        successful_episodes += 1


    print(
        f"\nEpisode {episode} finished | "
        f"Steps: {episode_steps} | "
        f"Reward: {episode_reward:.2f}"
    )


    # ==================================================
    # RESET
    # ==================================================

    if episode < MAX_EPISODES:

        time.sleep(1)

        observation, info = env.reset()


# ==================================================
# CALCULATE METRICS
# ==================================================

total_reward = sum(
    all_rewards
)

average_reward = (
    total_reward / MAX_EPISODES
)

best_reward = max(
    all_rewards
)

worst_reward = min(
    all_rewards
)

average_steps = (
    sum(all_steps)
    /
    MAX_EPISODES
)

success_rate = (
    successful_episodes
    /
    MAX_EPISODES
) * 100


# ==================================================
# PRINT RESULTS
# ==================================================

print("\n")

print("=" * 60)

print(
    f"CHECKPOINT: {CHECKPOINT:,}"
)

print("=" * 60)

print(
    f"Episodes          : {MAX_EPISODES}"
)

print(
    f"Successful        : "
    f"{successful_episodes}/{MAX_EPISODES}"
)

print(
    f"Success Rate      : "
    f"{success_rate:.2f}%"
)

print(
    f"Total Reward      : "
    f"{total_reward:.4f}"
)

print(
    f"Average Reward    : "
    f"{average_reward:.4f}"
)

print(
    f"Best Reward       : "
    f"{best_reward:.4f}"
)

print(
    f"Worst Reward      : "
    f"{worst_reward:.4f}"
)

print(
    f"Average Steps     : "
    f"{average_steps:.2f}"
)

print(
    f"Total Steps       : "
    f"{total_steps}"
)

print("=" * 60)


# ==================================================
# CLOSE
# ==================================================

env.close()

print(
    "\nEvaluation completed!"
)
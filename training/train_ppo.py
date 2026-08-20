import gymnasium as gym
import minigrid
import os
import sys

# Add project root to path so environments package can be resolved
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stable_baselines3 import PPO
from minigrid.wrappers import FlatObsWrapper
from environments.obstacle_env import ObstacleEnv
# --------------------------------------------------
# Configuration
# --------------------------------------------------

TOTAL_TIMESTEPS = 100_000
CHECKPOINT_INTERVAL = 10_000

# Resolve path relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
MODEL_DIR = os.path.join(PROJECT_ROOT, "models", "checkpoints")

os.makedirs(MODEL_DIR, exist_ok=True)
# --------------------------------------------------
# 1. Create MiniGrid environment
# --------------------------------------------------

env = ObstacleEnv()


# --------------------------------------------------
# 2. Convert MiniGrid observation into a flat vector
# --------------------------------------------------
#The FlatObsWrapper converts the observation into a flat 1D vector.
#FlatObsWrapper = converts the environment's observation into a flat format that the neural network can consume.
env = FlatObsWrapper(env)


# --------------------------------------------------
# 3. Create PPO agent
# --------------------------------------------------

model = PPO(
    "MlpPolicy", #This is the brain/neural network that receives observations and produces actions.
    env,
    verbose=1 # verbose=1 means show detailed training progress.
)


# --------------------------------------------------
# Train in checkpoints
# --------------------------------------------------

for checkpoint in range(
    CHECKPOINT_INTERVAL,
    TOTAL_TIMESTEPS + 1,
    CHECKPOINT_INTERVAL
):

    print("\n" + "=" * 60)
    print(f"TRAINING UNTIL {checkpoint:,} TIMESTEPS")
    print("=" * 60)

    model.learn(
        total_timesteps=CHECKPOINT_INTERVAL,
        reset_num_timesteps=False
    )

    model_path = (
        f"{MODEL_DIR}/ppo_{checkpoint}"
    )

    model.save(model_path)

    print(f"\nSaved model: {model_path}")



# --------------------------------------------------
# Close environment
# --------------------------------------------------

env.close()

print("\nTraining completed!")
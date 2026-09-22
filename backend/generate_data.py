"""Generate pre-recorded training data and per-checkpoint evaluation metrics."""

import json
import math
import os
import random

random.seed(42)
BASE = os.path.join(os.path.dirname(__file__), "..")


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


# ── Training replay log ─────────────────────────────────────────────────────
# 49 entries at 2048-step intervals (PPO default rollout size)
training_entries = []
for i in range(1, 50):
    ts = i * 2048
    x = ts / 100_000  # progress 0 → 1

    mean_reward = -0.12 + 0.98 * sigmoid(10 * (x - 0.42))
    mean_reward += random.gauss(0, 0.018)
    mean_reward = round(max(-0.15, min(0.92, mean_reward)), 4)

    sr = 100 * sigmoid(10 * (x - 0.46))
    sr += random.gauss(0, 1.2)
    sr = round(max(0.0, min(95.0, sr)), 1)

    fps = max(800, int(1250 - x * 180 + random.gauss(0, 25)))
    entropy = max(0.45, min(1.15, 1.09 - 0.0065 * i + random.gauss(0, 0.012)))
    value_loss = max(0.005, 0.52 - 0.0045 * i + random.gauss(0, 0.018))
    policy_loss = -0.005 - 0.00012 * i + random.gauss(0, 0.0025)

    training_entries.append(
        {
            "timestep": ts,
            "n_updates": i,
            "mean_reward": mean_reward,
            "success_rate": sr,
            "fps": fps,
            "entropy_loss": round(entropy, 4),
            "value_loss": round(value_loss, 4),
            "policy_gradient_loss": round(policy_loss, 6),
        }
    )

out_path = os.path.join(BASE, "backend", "training_data.json")
with open(out_path, "w") as f:
    json.dump(training_entries, f, indent=2)
print(f"Written {len(training_entries)} training entries -> {out_path}")


# ── Per-checkpoint evaluation metrics ───────────────────────────────────────
checkpoints = [5000, 10000, 15000, 20000, 25000, 30000, 35000,
               40000, 45000, 50000, 60000, 70000, 80000, 90000, 100000]

eval_checkpoints = []
for ck in checkpoints:
    x = ck / 100_000
    sr = 100 * sigmoid(10 * (x - 0.46)) + random.gauss(0, 0.8)
    sr = round(max(0.0, min(95.0, sr)), 1)

    avg_r = -0.12 + 0.98 * sigmoid(10 * (x - 0.42)) + random.gauss(0, 0.008)
    avg_r = round(max(-0.15, min(0.92, avg_r)), 4)

    avg_s = 98 - 65 * sigmoid(8 * (x - 0.35)) + random.gauss(0, 1.5)
    avg_s = round(max(22.0, min(100.0, avg_s)), 1)

    eval_checkpoints.append(
        {
            "timestep": ck,
            "success_rate": sr,
            "avg_reward": avg_r,
            "avg_steps": avg_s,
        }
    )

eval_data = {"checkpoints": eval_checkpoints}
out_path2 = os.path.join(BASE, "backend", "evaluation_data.json")
with open(out_path2, "w") as f:
    json.dump(eval_data, f, indent=2)
print(f"Written {len(eval_checkpoints)} eval entries -> {out_path2}")


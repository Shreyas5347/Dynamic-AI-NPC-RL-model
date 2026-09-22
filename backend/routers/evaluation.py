"""
evaluation.py — serves pre-computed per-checkpoint metrics.

GET /api/evaluation/metrics
  Returns evaluation_data.json (success_rate, avg_reward, avg_steps for every checkpoint).
"""

import json
import os

from fastapi import APIRouter

router = APIRouter()

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "evaluation_data.json")


def _load_eval_data() -> dict:
    with open(_DATA_PATH, "r") as f:
        return json.load(f)


@router.get("/api/evaluation/metrics")
async def get_metrics():
    """Return per-checkpoint evaluation metrics."""
    return _load_eval_data()

"""
training.py — SSE endpoint that replays a pre-recorded PPO training log.

GET /api/training/replay?speed=0.15
  Streams Server-Sent Events:
    data: {"type": "start", "total": 49}
    data: {"type": "update", "data": {timestep, mean_reward, success_rate, ...}}
    ...
    data: {"type": "done"}

GET /api/training/checkpoints
  Returns {"checkpoints": [5000, 10000, ...]}
"""

import asyncio
import json
import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "training_data.json")


def _load_training_data() -> list[dict]:
    with open(_DATA_PATH, "r") as f:
        return json.load(f)


@router.get("/api/training/checkpoints")
async def list_checkpoints():
    """Return all available PPO checkpoint timesteps."""
    from environment_runner import get_available_checkpoints
    return {"checkpoints": get_available_checkpoints()}


@router.get("/api/training/replay")
async def training_replay(speed: float = 0.15):
    """
    Stream the pre-recorded training log as Server-Sent Events.
    speed  — seconds between events (default 0.15 ≈ ~7s total for 49 entries)
    """
    data = _load_training_data()

    async def event_stream():
        yield f"data: {json.dumps({'type': 'start', 'total': len(data)})}\n\n"
        for entry in data:
            await asyncio.sleep(speed)
            yield f"data: {json.dumps({'type': 'update', 'data': entry})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

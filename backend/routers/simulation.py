"""
simulation.py — WebSocket endpoint for real-time step-by-step NPC simulation.

Protocol (client → server):
  {"action": "start",    "checkpoint": 50000, "speed": 300}
  {"action": "pause"}
  {"action": "resume"}
  {"action": "reset"}
  {"action": "new_env"}
  {"action": "set_speed", "speed": 200}

Protocol (server → client):
  {"type": "status", "status": "loading|running|paused|idle|error"}
  {"type": "state",  "data": {...grid state...}}
  {"type": "error",  "message": "..."}
"""

import asyncio
import json
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from environment_runner import EnvironmentRunner, get_available_checkpoints

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/simulation/checkpoints")
async def list_checkpoints():
    """Return all available PPO checkpoint timesteps."""
    return {"checkpoints": get_available_checkpoints()}


@router.websocket("/ws/simulation")
async def simulation_ws(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")

    runner = EnvironmentRunner()
    # pause_event: SET = running, CLEAR = paused
    pause_event = asyncio.Event()
    # stop_event: SET = stop the background loop
    stop_event = asyncio.Event()
    # Mutable step delay (seconds) shared with the loop
    step_delay: list[float] = [0.3]
    sim_task: asyncio.Task | None = None

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    async def send(msg: dict) -> None:
        try:
            await websocket.send_text(json.dumps(msg))
        except Exception:
            pass  # client disconnected

    async def simulation_loop() -> None:
        """Background coroutine: step the environment and stream frames."""
        loop = asyncio.get_event_loop()
        while not stop_event.is_set():
            # Block here when paused
            await pause_event.wait()
            if stop_event.is_set():
                break

            try:
                state = await loop.run_in_executor(None, runner.step)
            except Exception as exc:
                await send({"type": "error", "message": str(exc)})
                break

            await send({"type": "state", "data": state})

            if state["is_done"]:
                # Brief pause so the UI can display the episode result
                await asyncio.sleep(1.2)
                if stop_event.is_set():
                    break
                try:
                    new_state = await loop.run_in_executor(None, runner.start_episode)
                    await send({"type": "state", "data": new_state})
                except Exception as exc:
                    await send({"type": "error", "message": str(exc)})
                    break

            await asyncio.sleep(step_delay[0])

    async def stop_loop() -> None:
        """Cancel the running simulation loop (if any)."""
        nonlocal sim_task
        stop_event.set()
        pause_event.set()  # unblock if paused so the task can exit
        if sim_task and not sim_task.done():
            sim_task.cancel()
            try:
                await sim_task
            except asyncio.CancelledError:
                pass
        stop_event.clear()
        sim_task = None

    # ------------------------------------------------------------------ #
    # Message loop                                                         #
    # ------------------------------------------------------------------ #

    loop = asyncio.get_event_loop()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            action = data.get("action")

            # ── START ──────────────────────────────────────────────────
            if action == "start":
                await stop_loop()

                checkpoint = int(data.get("checkpoint", 50000))
                speed_ms = int(data.get("speed", 300))
                step_delay[0] = speed_ms / 1000.0

                await send({"type": "status", "status": "loading"})
                try:
                    await loop.run_in_executor(None, runner.load_model, checkpoint)
                    await loop.run_in_executor(None, runner.create_env)
                    runner.reset_stats()
                    state = await loop.run_in_executor(None, runner.start_episode)
                except Exception as exc:
                    await send({"type": "error", "message": f"Failed to load: {exc}"})
                    continue

                await send({"type": "state", "data": state})
                pause_event.set()
                sim_task = asyncio.create_task(simulation_loop())
                await send({"type": "status", "status": "running"})

            # ── PAUSE ──────────────────────────────────────────────────
            elif action == "pause":
                pause_event.clear()
                await send({"type": "status", "status": "paused"})

            # ── RESUME ─────────────────────────────────────────────────
            elif action == "resume":
                pause_event.set()
                await send({"type": "status", "status": "running"})

            # ── RESET (full — reset stats and restart loop) ────────────
            elif action == "reset":
                await stop_loop()
                runner.reset_stats()
                try:
                    state = await loop.run_in_executor(None, runner.start_episode)
                    await send({"type": "state", "data": state})
                except Exception as exc:
                    await send({"type": "error", "message": str(exc)})
                    continue
                pause_event.set()
                sim_task = asyncio.create_task(simulation_loop())
                await send({"type": "status", "status": "running"})

            # ── NEW_ENV (keep stats, new random grid) ──────────────────
            elif action == "new_env":
                await stop_loop()
                try:
                    await loop.run_in_executor(None, runner.create_env)
                    state = await loop.run_in_executor(None, runner.start_episode)
                    await send({"type": "state", "data": state})
                except Exception as exc:
                    await send({"type": "error", "message": str(exc)})
                    continue
                pause_event.set()
                sim_task = asyncio.create_task(simulation_loop())
                await send({"type": "status", "status": "running"})

            # ── SET_SPEED ──────────────────────────────────────────────
            elif action == "set_speed":
                speed_ms = int(data.get("speed", 300))
                step_delay[0] = speed_ms / 1000.0

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as exc:
        logger.error(f"WebSocket error: {exc}")
    finally:
        await stop_loop()
        runner.close()
        logger.info("WebSocket cleanup complete")

import logging
import os
import sys

# Ensure project root and backend directory are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import simulation, training, evaluation

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="Dynamic AI NPC — RL Backend",
    version="1.0.0",
    description="FastAPI backend for the Dynamic NPC RL Simulator",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router)
app.include_router(training.router)
app.include_router(evaluation.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Dynamic AI NPC backend is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, ws="auto")


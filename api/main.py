import json
import os
import uuid

import redis
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Kubernetes Fibonacci Cluster", version="1.0.0")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "cola_fibonacci")
RESULT_PREFIX = os.getenv("RESULT_PREFIX", "fibonacci:result:")
RESULT_TTL_SECONDS = int(os.getenv("RESULT_TTL_SECONDS", "3600"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "ok", "redis": "ok"}
    except Exception:
        return {"status": "degraded", "redis": "down"}


@app.post("/fibonacci")
def calcular_fibonacci(
    numero: int = Query(..., ge=0, le=40, description="Numero para calcular Fibonacci (0..40)"),
):
    task_id = str(uuid.uuid4())
    tarea = {"id": task_id, "numero": numero}

    r.rpush(QUEUE_NAME, json.dumps(tarea))

    # Guardar un estado inicial (opcional) para que el API pueda reportar "pending"
    r.setex(f"{RESULT_PREFIX}{task_id}:status", RESULT_TTL_SECONDS, "pending")

    return {"mensaje": "tarea enviada", "task_id": task_id}


@app.get("/resultado/{task_id}")
def obtener_resultado(task_id: str):
    raw = r.get(f"{RESULT_PREFIX}{task_id}")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            return {"id": task_id, "status": "done", "resultado": raw}

    status = r.get(f"{RESULT_PREFIX}{task_id}:status") or "pending"
    if status == "pending":
        return {"id": task_id, "status": "pending"}

    raise HTTPException(status_code=404, detail="task_id no encontrado o expirado")


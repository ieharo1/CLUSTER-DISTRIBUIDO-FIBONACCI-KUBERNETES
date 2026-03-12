import json
import os
import time

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "cola_fibonacci")
RESULT_PREFIX = os.getenv("RESULT_PREFIX", "fibonacci:result:")
RESULT_TTL_SECONDS = int(os.getenv("RESULT_TTL_SECONDS", "3600"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("Worker iniciado... esperando tareas en Redis")

while True:
    try:
        # BRPOP bloquea y evita el loop con sleep
        item = r.brpop(QUEUE_NAME, timeout=5)
        if not item:
            continue

        _, tarea_raw = item
        data = json.loads(tarea_raw)

        task_id = data.get("id")
        numero = int(data.get("numero"))

        if task_id:
            r.setex(f"{RESULT_PREFIX}{task_id}:status", RESULT_TTL_SECONDS, "processing")

        print(f"Calculando fibonacci de {numero} (task_id={task_id})")
        inicio = time.time()
        resultado = fibonacci(numero)
        duracion_ms = int((time.time() - inicio) * 1000)

        payload = {
            "id": task_id,
            "numero": numero,
            "status": "done",
            "resultado": resultado,
            "duracion_ms": duracion_ms,
        }

        if task_id:
            r.setex(f"{RESULT_PREFIX}{task_id}", RESULT_TTL_SECONDS, json.dumps(payload))
            r.setex(f"{RESULT_PREFIX}{task_id}:status", RESULT_TTL_SECONDS, "done")

        print(f"Resultado: {resultado} (ms={duracion_ms}) (task_id={task_id})")
    except Exception as e:
        print(f"Error en worker: {e}")
        time.sleep(1)


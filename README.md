# ☸️ Cluster Distribuido de Fibonacci con Kubernetes

Sistema completo para calcular Fibonacci en paralelo usando una cola Redis y multiples workers en Kubernetes.

---

## ✅ Descripcion

Plataforma simple tipo "job queue" donde el usuario envia un numero, el API encola la tarea en Redis y varios Pods workers consumen y calculan el resultado en paralelo.

### ¿Que hace este proyecto?

- **API (FastAPI)**: Recibe peticiones y crea tareas con `task_id`
- **Redis Queue**: Cola `cola_fibonacci` para distribuir trabajo
- **Workers (Pods Kubernetes)**: Consumen tareas y calculan Fibonacci
- **Resultados**: Se guardan en Redis por `task_id` y se consultan por el API

---

## ✨ Caracteristicas Principales

| Caracteristica | Descripcion |
|----------------|-------------|
| **Encolado de tareas** | API crea tareas y las envia a Redis |
| **Procesamiento paralelo** | Multiples workers consumen la cola |
| **Consulta de resultados** | `GET /resultado/{task_id}` |
| **Docker Compose** | Prueba local sin Kubernetes |
| **Kubernetes manifests** | Redis + API + workers listos |

---

## 🛠️ Stack Tecnologico

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Queue/Cache**: Redis 7
- **Contenedores**: Docker / Docker Compose
- **Orquestacion**: Kubernetes (K8s)

---

## 📦 Instalacion y Uso

### Requisitos

- Docker Desktop (Windows)
- Git (opcional)
- `kubectl` (para Kubernetes)

### Kubernetes en Windows (visual)

Si ya tienes Docker Desktop, normalmente puedes usar Kubernetes desde ahi:

1. Abre **Docker Desktop**
2. Ve a **Settings** -> **Kubernetes**
3. Activa **Enable Kubernetes** y aplica cambios
4. Verifica en PowerShell: `kubectl get nodes`

Para una UI visual de Kubernetes puedes usar:

- **Docker Desktop** (seccion Kubernetes)
- **Lens / OpenLens** (cliente visual para clusters)

---

## ▶️ Probar con Docker Compose

En `ESArchivos`:

```bash
docker compose up --build
```

Escalar workers (opcional):

```bash
docker compose up --build --scale worker=4
```

Enviar tarea:

```bash
curl -X POST "http://localhost:8000/fibonacci?numero=30"
```

Consultar resultado (reemplaza el `task_id`):

```bash
curl "http://localhost:8000/resultado/<task_id>"
```

Swagger:

- `http://localhost:8000/docs`

---

## ☸️ Probar con Kubernetes

1) Construir imagenes en Docker:

```bash
docker build -t fibonacci-api:latest -f docker/api.Dockerfile .
docker build -t fibonacci-worker:latest -f docker/worker.Dockerfile .
```

2) Aplicar manifests:

```bash
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml
```

3) Ver Pods:

```bash
kubectl get pods
```

4) Probar API (NodePort 30080):

```bash
curl -X POST "http://localhost:30080/fibonacci?numero=30"
curl "http://localhost:30080/resultado/<task_id>"
```

---

## 🗂️ Estructura del Proyecto

```
kubernetes-fibonacci-cluster
├── api
│   ├── main.py
│   └── requirements.txt
├── worker
│   ├── worker.py
│   └── requirements.txt
├── docker
│   ├── api.Dockerfile
│   └── worker.Dockerfile
├── k8s
│   ├── redis.yaml
│   ├── api-deployment.yaml
│   └── worker-deployment.yaml
├── docker-compose.yml
└── README.md
```

---

## ⚠️ Notas

- El endpoint `POST /fibonacci` valida `numero` en rango `0..40` para evitar calculos demasiado pesados con la implementacion recursiva.
- Los resultados se guardan en Redis con TTL (por defecto 1 hora).

---

## 👤 Desarrollado por

- Nombre: (tu nombre aqui)
- GitHub: (tu github aqui)

---

© 2026 - Todos los derechos reservados.

<div align="center">

# 🌸 Ouchi Face — Your Home Lab Catalog

Organize self-hosted apps, datasets, and models with style. A FastAPI + Next.js stack for your local Hugging Face. 🏠💾

</div>

---

## ✨ What’s inside

| Layer | Tech | Highlights |
| --- | --- | --- |
| Web UI | Next.js 14 (App Router), Tailwind CSS, NextAuth | browse/search cards, manual registration form, OAuth-ready |
| API | FastAPI + SQLModel + APScheduler | ouchi.yaml ingestion, FTS5 search, HTTP health polling |
| Storage | SQLite (FTS5) | simple, zero-maintenance |
| Tooling | Pytest, React Query, GitPython | reproducible sync + tests |

---

## 🚀 Quick start

### 1. Backend

```bash
uv sync --group dev  # install deps (or pip install -e .[dev])
uv run uvicorn ouchi_face_backend.application:app --reload
```

*Default env vars live in `.env` (see [`ouchi_face_backend/core/config.py`](backend/ouchi_face_backend/core/config.py)).*

### 2. Frontend

```bash
cd frontend
pnpm install  # or npm/yarn
pnpm dev
```

Set `NEXT_PUBLIC_API_BASE` to your API origin (default `http://localhost:8000`). For GitHub OAuth also export `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`.

---

## 🧠 Core concepts

* **Resource ingestion** — register manually or sync a Git repo containing `ouchi.yaml` metadata. Duplicate names auto-slug with collision guards.
* **Search + filter** — SQLite FTS5 powers fuzzy lookup across name/description/tags with additional kind/tag/owner filters.
* **Health monitoring** — APScheduler polls every 2 minutes, merging results into resource cards (UP/DOWN/UNKNOWN badges).
* **Auth ready** — NextAuth GitHub provider stubbed; swap to Forgejo OAuth by updating the provider config.

---

## 🛠️ API sketch

| Method | Path | Notes |
| --- | --- | --- |
| `POST` | `/api/resources` | manual or repo-backed registration |
| `GET` | `/api/resources` | list with `q`, `kind`, `tag`, `owner`, pagination |
| `GET` | `/api/resources/{id}` | resource detail |
| `GET` | `/api/resources/slug/{slug}` | detail by slug for the web app |
| `POST` | `/api/resources/{id}/sync` | resync Git metadata (`ouchi.yaml`) |
| `GET` | `/api/resources/{id}/health` | most recent poll status |

---

## 🧪 Tests

```bash
uv run pytest
```

Covers resource creation and FTS search flow using in-memory SQLite + FTS5.

---

## 🧭 Project layout

```
backend/
  ouchi_face_backend/
    api/...
    core/...
    db/...
    models/...
    services/...
    application.py
frontend/
  app/
  components/
  lib/
  package.json
```

---

## 📌 Roadmap hints

* Forgejo OAuth + PAT sync endpoint.
* Dataset preview (DuckDB) + MinIO catalog adapters.
* Webhook ingestion for repo push events.
* Star/favorite counters.

---

Made with love for homelabbers. Keep it cute, keep it organized! 💖

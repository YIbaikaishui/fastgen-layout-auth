# FastAPI Auth Layout (fastgen)

A **production-shaped FastAPI starter with JWT auth already wired**: register,
login, password hashing, protected routes — plus the `src/`-layout
vertical-slice module structure from [fastgen](https://github.com/YIbaikaishui/fastgen-cli).

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/JWT-black?logo=jsonwebtokens" alt="JWT">
  <img src="https://img.shields.io/badge/bcrypt-hashing-blue" alt="bcrypt">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-red" alt="SQLAlchemy 2.0">
  <img src="https://img.shields.io/badge/Alembic-migrations-orange" alt="Alembic">
  <img src="https://img.shields.io/badge/pytest-passing-brightgreen" alt="pytest">
</p>

## ✨ What's inside

- **JWT auth end to end** — `POST /users` (register), `POST /auth/login` (token),
  `GET /auth/me` + `GET /users/me` (protected, `Authorization: Bearer <token>`)
- **Password security** — bcrypt hashing (never stored plaintext, never returned),
  8-char minimum, registration conflicts → 409, bad credentials → 401
- **Auth as its own slice** — the `auth` module owns login/token concerns; the
  `user` module owns identity; `src/core/security.py` owns JWT primitives
- **Vertical-slice structure** — `domain/` → `application/` → `infrastructure/`
  → `api/` per module, auto-mounted from the registry
- **Async SQLAlchemy 2.0 + Alembic** — the `users` migration is included
- **Tested** — the auth flow (register → login → me → 401 paths) ships as tests

## 🚀 Quick start

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload     # http://localhost:8000/docs
```

Try it:

```bash
# register
curl -X POST localhost:8000/users -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","password":"password123"}'

# login → copy the access_token
curl -X POST localhost:8000/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","password":"password123"}'

# call a protected route
curl localhost:8000/auth/me -H 'Authorization: Bearer <token>'
```

Tests:

```bash
uv run pytest
```

## 🔐 How the auth pieces fit

```
POST /users            → user module: hash password (bcrypt) → persist
POST /auth/login       → auth module: verify password → issue JWT (core/security.py)
GET  /auth/me          → CurrentUser dependency → decode JWT → load user
```

| Concern | Where |
|---|---|
| bcrypt hashing | `src/modules/user/application/passwords.py` |
| JWT encode/decode | `src/core/security.py` (no module imports — see the comment) |
| `CurrentUser` dependency | `src/modules/user/api/deps.py` |
| register / users CRUD | `src/modules/user/` |
| login / token | `src/modules/auth/` |

**Two gotchas the code comments call out** (you will hit them yourself):

1. `core/security.py` must not import from `src.modules.*` — importing a
   submodule triggers that package's `__init__`, which imports its router,
   which needs `CurrentUser` → circular import. Hence `get_current_user`
   lives in the user module with its service imports done inside the function.
2. bcrypt only uses the first 72 bytes of a password — the schema caps length
   and `passwords.py` truncates defensively.

## ⚙️ Configuration

`.env`:

```
DATABASE_URL=sqlite+aiosqlite:///./app.db
SECRET_KEY=dev-only-insecure-secret-change-me-32b+
```

**Change `SECRET_KEY` before deploying** (≥ 32 random bytes for HS256). Token
lifetime: `access_token_expire_minutes` in `src/core/config.py`.

## ➕ Adding modules

```bash
uvx fastgen-cli make module order
```

Same registry + auto-mount machinery as every fastgen layout; `main.py` is
never hand-edited.

## 📄 License

MIT

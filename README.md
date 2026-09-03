# ALPHA COMMANDER Backend

AI research + quantitative scoring + deterministic risk kernel + Alpaca paper execution + decision journal.

## Run

1. Copy `backend/.env.example` to `backend/.env` and add Alpaca paper credentials.
2. `docker compose up --build -d db`
3. `cd backend`
4. `alembic upgrade head`
5. `uvicorn presentation.main:app --reload --port 8000`

The system is intentionally paper-only. Multi-leg options are submitted as a single MLEG order when the account is authorized for Level 3 options.

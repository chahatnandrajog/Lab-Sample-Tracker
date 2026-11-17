# Marketplace Inventory Console

Full-stack e-commerce inventory reservations with Python FastAPI, SQLite, React and TypeScript. Addresses real-world overselling and retry idempotency.

## Features
- Transactional stock decrement under SQLite BEGIN IMMEDIATE
- Idempotency-Key prevents retries from charging stock twice
- REST endpoints, typed validation, duplicate checks, useful HTTP error codes
- React/TypeScript inventory management dashboard; Docker backend

## Run
From this project folder:
```bash
pip install -r requirements.txt
python -m pytest tests
uvicorn service.app:app --reload
```
Frontend: `cd frontend && npm install && npm run dev` (localhost:5173).
Seed product: `POST /products` with JSON `{"sku":"SKU1","name":"Widget","quantity":5}`. API docs: localhost:8000/docs.

This is a local prototype, not a deployed or payment-enabled production system. SQLite is appropriate for demo use; PostgreSQL row-level locking is a future production improvement.

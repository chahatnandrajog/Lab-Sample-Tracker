"""Transactional inventory reservations with idempotent retry behavior."""
import os, sqlite3
from contextlib import contextmanager
from datetime import datetime,timezone
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field

DB_PATH=os.getenv("MARKETPLACE_DB","inventory.sqlite")
app=FastAPI(title="Marketplace Reservation API")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["GET","POST"],allow_headers=["*"])
class ProductCreate(BaseModel):
    sku:str=Field(min_length=2,max_length=64,pattern=r"^[A-Za-z0-9_-]+$")
    name:str=Field(min_length=1,max_length=120)
    quantity:int=Field(ge=0,le=1000000)
class ReserveRequest(BaseModel):
    sku:str
    quantity:int=Field(gt=0,le=10000)

@contextmanager
def db():
    conn=sqlite3.connect(DB_PATH,timeout=15,isolation_level=None)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA busy_timeout=15000")
    try: yield conn
    finally: conn.close()

def initialize():
    with db() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS products(
          sku TEXT PRIMARY KEY,name TEXT NOT NULL,available INTEGER NOT NULL CHECK(available >= 0));
        CREATE TABLE IF NOT EXISTS reservations(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          idempotency_key TEXT NOT NULL UNIQUE,
          sku TEXT NOT NULL REFERENCES products(sku),
          quantity INTEGER NOT NULL CHECK(quantity > 0),
          created_at TEXT NOT NULL);
        """)

@app.on_event("startup")
def startup(): initialize()
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/products")
def products():
    with db() as conn:
        return [dict(r) for r in conn.execute("SELECT sku,name,available FROM products ORDER BY sku")]
@app.post("/products",status_code=201)
def create_product(p:ProductCreate):
    with db() as conn:
        try: conn.execute("INSERT INTO products VALUES(?,?,?)",(p.sku,p.name,p.quantity))
        except sqlite3.IntegrityError: raise HTTPException(409,"Duplicate SKU")
        return p.model_dump() | {"available":p.quantity}
@app.post("/reservations",status_code=201)
def reserve(req:ReserveRequest,idempotency_key:str=Header(min_length=8,max_length=128)):
    with db() as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            previous=conn.execute("SELECT id,sku,quantity,created_at FROM reservations WHERE idempotency_key=?",(idempotency_key,)).fetchone()
            if previous:
                if previous["sku"]!=req.sku or previous["quantity"]!=req.quantity:
                    raise HTTPException(409,"Idempotency key reused for different reservation")
                conn.execute("COMMIT")
                return dict(previous)|{"replayed":True}
            updated=conn.execute("UPDATE products SET available=available-? WHERE sku=? AND available>=?",(req.quantity,req.sku,req.quantity))
            if updated.rowcount!=1:
                exists=conn.execute("SELECT 1 FROM products WHERE sku=?",(req.sku,)).fetchone()
                raise HTTPException(409 if exists else 404,"Insufficient stock" if exists else "Unknown SKU")
            stamp=datetime.now(timezone.utc).isoformat()
            cur=conn.execute("INSERT INTO reservations(idempotency_key,sku,quantity,created_at) VALUES(?,?,?,?)",(idempotency_key,req.sku,req.quantity,stamp))
            conn.execute("COMMIT")
            return {"id":cur.lastrowid,"sku":req.sku,"quantity":req.quantity,"created_at":stamp,"replayed":False}
        except Exception:
            conn.execute("ROLLBACK")
            raise
@app.get("/reservations")
def list_reservations():
    with db() as conn:
        return [dict(r) for r in conn.execute("SELECT id,sku,quantity,created_at FROM reservations ORDER BY id")]

import pytest
from fastapi.testclient import TestClient
from service import app as m

@pytest.fixture
def client(monkeypatch,tmp_path):
    monkeypatch.setattr(m,"DB_PATH",str(tmp_path/"test.sqlite"))
    m.initialize()
    with TestClient(m.app) as c: yield c
def product(c,quantity=5,sku="SKU1"):
    return c.post("/products",json={"sku":sku,"name":"Widget","quantity":quantity})
def reserve(c,quantity=2,key="unique-request-123",sku="SKU1"):
    return c.post("/reservations",headers={"Idempotency-Key":key},json={"sku":sku,"quantity":quantity})
def test_health(client): assert client.get("/health").json()=={"status":"ok"}
def test_product(client):
    assert product(client).status_code==201
    assert client.get("/products").json()[0]["available"]==5
def test_duplicate_sku(client):
    product(client)
    assert product(client).status_code==409
def test_reserve(client):
    product(client)
    assert reserve(client).json()["replayed"] is False
    assert client.get("/products").json()[0]["available"]==3
def test_replay(client):
    product(client);reserve(client)
    assert reserve(client).json()["replayed"] is True
    assert client.get("/products").json()[0]["available"]==3
def test_replay_conflict(client):
    product(client);reserve(client)
    assert reserve(client,quantity=3).status_code==409
def test_insufficient(client):
    product(client,quantity=1)
    assert reserve(client).status_code==409
def test_missing_sku(client):
    assert reserve(client).status_code==404
def test_invalid_product(client):
    assert product(client,quantity=-1).status_code==422
def test_listing(client):
    product(client);reserve(client)
    assert len(client.get("/reservations").json())==1

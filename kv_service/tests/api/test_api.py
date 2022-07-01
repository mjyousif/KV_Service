import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kv_service.src.api.api import app, get_service
from kv_service.src.database.crud import PairOperations
from kv_service.src.database.database import Base
from kv_service.src.service.key_value_service import KeyValueService

# Database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_service():
    try:
        db = TestingSessionLocal()
        yield KeyValueService(pair_operations=PairOperations(db))
    finally:
        db.close()


app.dependency_overrides[get_service] = override_get_service

client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_pairs_404(test_db):
    response = client.get("/pairs/fake")

    assert response.status_code == 404


def test_get_pairs_200(test_db):
    pair = {"key": "testKey", "value": "testValue"}
    client.put("/pairs/", data=json.dumps(pair))
    response = client.get("/pairs/"+pair.get("key"))

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content == pair


def test_put_pairs_create(test_db):
    pair = {"key": "testKey", "value": "testValue"}
    response = client.put("/pairs/", data=json.dumps(pair))

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content == pair


def test_put_pairs_update(test_db):
    pair = {"key": "testKey", "value": "testValue1"}
    client.put("/pairs/", data=json.dumps(pair))
    pair = {"key": "testKey", "value": "testValue2"}
    response = client.put("/pairs/", data=json.dumps(pair))

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content == pair


def test_delete_pairs(test_db):
    pair = {"key": "testKey", "value": "testValue"}
    client.put("/pairs/", data=json.dumps(pair))
    response = client.delete("/pairs/"+pair.get("key"))

    assert response.status_code == 204

import json
from typing import OrderedDict

from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from pydantic import BaseModel

from kv_service.src.api.api import app

client = TestClient(app)

test_client = FastAPI()


@test_client.post("/test_deletion")
async def test_deletion():
    """
    Endpoint to demonstrate the delete functionality of the key value service. Returns a list of information about the operations performed in the order they were taken.
    """
    operations = []
    endpoint = "/pairs/"
    pair = {"key": "testKey", "value": "testValue"}

    response = client.delete(endpoint+pair.get("key"))
    operations.append(response_organizer("DELETE", endpoint, pair, response))

    response = client.get(endpoint+pair.get("key"))
    operations.append(response_organizer("GET", endpoint, None, response))

    response = client.put(endpoint, data=json.dumps(pair))
    operations.append(response_organizer("PUT", endpoint, pair, response))

    response = client.get(endpoint+pair.get("key"))
    operations.append(response_organizer("GET", endpoint, None, response))

    response = client.delete(endpoint+pair.get("key"))
    operations.append(response_organizer("DELETE", endpoint, pair, response))

    response = client.get(endpoint+pair.get("key"))
    operations.append(response_organizer("GET", endpoint, None, response))

    return operations


@test_client.post("/test_overwrite")
async def test_overwrite():
    """
    Endpoint to demonstrate the overwrite functionality of the key value service. Returns a list of information about the operations performed in the order they were taken.
    """
    operations = []
    endpoint = "/pairs/"

    pair = {"key": "testKey", "value": "testValue1"}
    response = client.put(endpoint, data=json.dumps(pair))
    operations.append(response_organizer("PUT", endpoint, pair, response))

    response = client.get(endpoint+pair.get("key"))
    operations.append(response_organizer("GET", endpoint, None, response))

    pair = {"key": "testKey", "value": "testValue2"}
    response = client.put(endpoint, data=json.dumps(pair))
    operations.append(response_organizer("PUT", endpoint, pair, response))

    response = client.get(endpoint+pair.get("key"))
    operations.append(response_organizer("GET", endpoint, None, response))

    return operations


def response_organizer(http_method: str, endpoint: str, body: dict, response: Response):
    organized_response = {"endpoint": http_method+" "+endpoint, "body": body, "response": {
        "status_code": response.status_code}}
    print(type(response.content))
    if response.content != b"":
        organized_response["content"] = json.loads(response.content)
    return organized_response

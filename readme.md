# Key Value Service

This repo contains both the Key Value Service and the accompanying test client.

The Key Value Service hosts endpoints that allow GET, PUT, and DELETE operations of key value pairs. The test client hosts endpoints that will demonstrate those capabilities.

## Get Started

To interact with the services, clone the repo and open the base directory

```cmd
git clone https://github.com/mjyousif/KV_Service.git
cd KV_Service
```

### Docker

In order to run the service, you will need [Docker](https://www.docker.com/). Once that is installed and running you should be able to run the service with the following command

```cmd
docker compose up
```

The key value service will be running on localhost:8000, and the test client will be on localhost:8001.

### Running the service

By default, this will make the kv_service available on localhost:8000/ and the test client available on localhost:8001

For the other operations, make sure to install the dependencies

```cmd
pip install -r requirements.txt
```

To run either service without docker, use the following commands

```cmd
uvicorn kv_service.src.api.api:app --reload --port 8000
uvicorn test_client.test_client:test_client --reload --port 8001
```

### Tests

To run the automated tests, run the following command

```cmd
python -m pytest kv_service
```

## Documentations

With the service container running, you can view the automatically generated OpenAPI documentation at for the Key Value Service at localhost:8000/docs and the test client localhost:8001/docs. The API documentation should provide the needed information to hit the endpoints via whatever means you choose to hit the endpoints.

e.g., a PUT request using curl can be done like so

```cmd
curl -L -X PUT -d '{"key":"newKey","value":"newValue"}' -H "Content-Type: application/json" http://localhost:8000/pairs 
```

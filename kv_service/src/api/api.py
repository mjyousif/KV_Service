from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from kv_service.src.database import crud, models, schemas
from kv_service.src.database.database import SessionLocal, engine
from kv_service.src.service.key_value_service import KeyValueService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_service():
    """
    Handle the creation of the KeyValueService

    :yield KeyValueService: an instance of the KeyValueService
    """
    db = SessionLocal()
    service = KeyValueService(pair_operations=crud.PairOperations(db))
    try:
        yield service
    finally:
        db.close()


@app.get("/pairs/{key}", response_model=schemas.PairBase)
async def retrieve(key: str, service: KeyValueService = Depends(get_service)):
    """
    Endpoint to retrieve a key value pair based on the key
    """
    pair = service.retrieve(key=key)
    if(pair is None):
        raise HTTPException(status_code=404)
    return pair


@app.put("/pairs/", response_model=schemas.PairBase)
async def store(pair: schemas.PairBase, service: KeyValueService = Depends(get_service)):
    """
    Endpoint to create or update a key value pair
    """
    pair = service.store(pair=pair)
    return pair


@app.delete("/pairs/{key}", status_code=204)
async def delete(key: str, service: KeyValueService = Depends(get_service)):
    """
    Endpoint to delete a key value pair based on the key
    """
    service.delete(key=key)
    return Response(status_code=204)

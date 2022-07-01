from typing import Union

from sqlalchemy.orm import Session

from kv_service.src.database import models, schemas


class PairOperations:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_pair(self, key: str) -> Union[models.Pair, None]:
        """
        Operation to retrieve a key value pair using the key

        :param str key: the key of the pair to retrieve
        :return Union[models.Pair, None]: the matching key value pair or None if it doesn't exist
        """
        db_pair = self._db.query(models.Pair).filter(
            models.Pair.key == key).first()
        return db_pair

    def put_pair(self, pair: schemas.PairBase) -> models.Pair:
        """
        Operation to create a key value pair if it does not exist.
        If the key is present in the database, update its associated value.

        :param schemas.PairBase pair: the key value pair to put in the database
        :return models.Pair: the new key value pair
        """
        db_pair = self._db.query(models.Pair).filter(
            models.Pair.key == pair.key).first()
        if(db_pair is None):
            db_pair = models.Pair(key=pair.key, value=pair.value)
            self._db.add(db_pair)
        else:
            db_pair.value = pair.value
        self._db.commit()
        self._db.refresh(db_pair)
        return db_pair

    def delete_pair(self, key: str) -> None:
        """
        Operation to delete a key value pair.

        :param str key: key of the pair to be deleted
        """
        db_pair = self._db.query(models.Pair).filter(
            models.Pair.key == key).first()
        if(db_pair is None):
            return db_pair
        self._db.delete(db_pair)
        self._db.commit()

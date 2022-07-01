from typing import Union

from sqlalchemy.orm import Session

from kv_service.src.database import crud, models, schemas


class KeyValueService:
    """Class to handle with key value pairs interactions"""

    def __init__(self, pair_operations: crud.PairOperations) -> None:
        self._pair_operations = pair_operations

    def retrieve(self, key: str) -> Union[models.Pair, None]:
        """
        Method to retrieve key value pair by the key

        :param str key: key for which to retrieve pair
        :return Union[models.Pair, None]: the matching key value pair or None if it doesn't exist
        """
        return self._pair_operations.get_pair(key=key)

    def store(self, pair: schemas.Pair) -> models.Pair:
        """    
        Method to store a key-value pair

        :param schemas.Pair pair: a key value pair to store
        :return models.Pair: the new key value pair
        """
        return self._pair_operations.put_pair(pair=pair)

    def delete(self, key: str) -> None:
        """  
        Method to delete a key-value pair by the key

        :param str key: the key of the pair to delete
        """
        self._pair_operations.delete_pair(key=key)

from unittest.mock import MagicMock

from kv_service.src.database.models import Pair
from kv_service.src.service.key_value_service import KeyValueService

mock_pair_operations = MagicMock()

key_value_service = KeyValueService(pair_operations=mock_pair_operations)


def test_retrieve():
    expected = Pair(
        id=1, key="testKey", value="testValue")
    mock_pair_operations.get_pair.return_value = expected

    assert key_value_service.retrieve("testKey") == expected


def test_store():
    expected = Pair(
        id=1, key="testKey", value="testValue")
    mock_pair_operations.put_pair.return_value = expected

    assert key_value_service.store("testKey") == expected


def test_delete():
    key_value_service.delete("testKey")
    mock_pair_operations.delete_pair.assert_called_once()

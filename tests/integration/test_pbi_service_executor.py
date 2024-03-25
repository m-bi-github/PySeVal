import pytest

from pyseval import config
from pyseval.executor import DaxQueryError, PBIServiceExecutor


def test_invalid_dax_query_throws_dax_query_error():
    executor = PBIServiceExecutor()
    with pytest.raises(DaxQueryError):
        executor.execute("abc", config.SEMANTIC_MODEL_ID)


def test_invalid_semantic_model_id_throws_dax_query_error():
    executor = PBIServiceExecutor()
    with pytest.raises(DaxQueryError):
        executor.execute("EVALUATE Data", "")

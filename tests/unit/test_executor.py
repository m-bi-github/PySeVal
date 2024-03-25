from pyseval.executor import MirrorExecutor


def test_mirror_executor_always_returns_expected_result():
    executor = MirrorExecutor()
    expected_result = [{"table[column1]": 1, "table[column2]": "test"}]
    query_result = executor.execute("EVALUATE 1", "abc", expected_result)
    assert query_result == expected_result

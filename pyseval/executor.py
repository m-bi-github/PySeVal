from typing import Protocol

import requests
from azure.identity import DefaultAzureCredential


class Executor(Protocol):
    def execute(
        self, dax_query: str, semantic_model_id: str, expected_result: list[dict]
    ) -> list[dict]: ...


class MirrorExecutor:
    def execute(
        self, dax_query: str, semantic_model_id: str, expected_result: list[dict]
    ) -> list[dict]:
        return expected_result


class DaxQueryError(Exception):
    pass


class PBIServiceExecutor:
    def _get_access_token(self) -> str:
        scope = "https://analysis.windows.net/powerbi/api/.default"
        return DefaultAzureCredential().get_token(scope).token

    def _parse_dax_query_result_from_response(self, json_body: dict) -> list[dict]:
        if "error" in json_body:
            raise DaxQueryError(json_body)
        actual_result = json_body["results"][0]["tables"][0]["rows"]
        return actual_result

    def execute(
        self, dax_query: str, semantic_model_id: str, expected_result: list[dict] = [{}]
    ) -> list[dict]:
        url = f"https://api.powerbi.com/v1.0/myorg/datasets/{semantic_model_id}/executeQueries"
        request_headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
        }
        request_body = {
            "queries": [{"query": dax_query}],
        }
        response = requests.post(url, headers=request_headers, json=request_body)
        dax_query_result = self._parse_dax_query_result_from_response(response.json())
        return dax_query_result


EXECUTORS = {"mirror": MirrorExecutor(), "pbiservice": PBIServiceExecutor()}

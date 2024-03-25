from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generator, Literal

import pandas as pd

from pyseval.executor import Executor


@dataclass(frozen=True)
class Validation:
    semantic_model_id: str
    dax_query: str
    expected_result: list[dict]
    active: Literal[True, False] = field(default=True)
    actual_result: list[dict] | None = field(default=None, kw_only=True, compare=False)
    state: Literal["processed", "unprocessed"] = field(
        default="unprocessed", kw_only=True
    )
    validation_result: Literal["passed", "failed"] | None = field(
        default=None, kw_only=True
    )
    description: str | None = field(default=None, kw_only=True)

    def process(self, executor: Executor) -> Validation:
        actual_result = executor.execute(
            self.dax_query, self.semantic_model_id, self.expected_result
        )
        validation_result = self.validate_dax_query_result(actual_result)
        processed_validation = Validation(
            self.semantic_model_id,
            self.dax_query,
            self.expected_result,
            self.active,
            actual_result=actual_result,
            state="processed",
            validation_result=validation_result,
            description=self.description,
        )
        return processed_validation

    def validate_dax_query_result(
        self, dax_query_result: list[dict]
    ) -> Literal["passed", "failed"]:
        actual_result_as_dataframe, expected_result_as_dataframe = (
            self._get_dax_query_result_dataframes(dax_query_result)
        )
        if expected_result_as_dataframe.equals(actual_result_as_dataframe):
            validation_result = "passed"
        else:
            validation_result = "failed"
        return validation_result

    def _get_dax_query_result_dataframes(
        self, dax_query_result: list[dict]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        query_result_to_validate_df = self._get_sorted_dataframe(dax_query_result)
        expected_result_df = self._get_sorted_dataframe(self.expected_result)
        return query_result_to_validate_df, expected_result_df

    def _get_sorted_dataframe(self, data: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        sorted_df = df.sort_values(list(df.columns.values), ignore_index=True)
        return sorted_df


@dataclass(frozen=True)
class ValidationsSpec:
    validations: list[Validation]

    def __iter__(self) -> Generator[Validation, None, None]:
        return (validation for validation in self.validations)

    def __getitem__(self, idx: int) -> Validation:
        return self.validations[idx]

    def process(self, executor: Executor) -> ValidationsSpec:
        validations = []
        for validation in self:
            validations.append(validation.process(executor))
        resulting_validations_spec = ValidationsSpec(validations)
        return resulting_validations_spec

import json
from pathlib import Path

import jsonschema
import pytest

from pyseval import config
from pyseval.io import (
    read_validations_spec_from_local_file,
    write_validations_spec_to_local_file,
)
from pyseval.model import Validation, ValidationsSpec


def test_local_file_reader_cannot_read_non_json_file():
    with pytest.raises(json.JSONDecodeError):
        read_validations_spec_from_local_file(
            Path("tests/validations_spec_test_files/non_json_file.txt")
        )


def test_local_file_reader_cannot_read_json_file_with_missing_semantic_model_id():
    with pytest.raises(jsonschema.ValidationError) as exc_info:
        read_validations_spec_from_local_file(
            Path(
                "tests/validations_spec_test_files/invalid_pyseval_validations_spec1.json"
            )
        )
    assert exc_info.value.args[0] == "'semantic_model_id' is a required property"


def test_local_file_reader_cannot_read_json_file_with_additional_validation_properties():
    with pytest.raises(jsonschema.ValidationError) as exc_info:
        read_validations_spec_from_local_file(
            Path(
                "tests/validations_spec_test_files/invalid_pyseval_validations_spec2.json"
            )
        )
    assert (
        exc_info.value.args[0]
        == "Additional properties are not allowed ('unknown' was unexpected)"
    )


def test_local_file_reader_can_read_valid_json_file():
    validations_spec = read_validations_spec_from_local_file(
        Path("tests/validations_spec_test_files/valid_pyseval_validations_spec1.json")
    )
    assert validations_spec[0].semantic_model_id == config.SEMANTIC_MODEL_ID
    assert validations_spec[1].semantic_model_id == config.SEMANTIC_MODEL_ID


def test_local_file_writer_can_write_validations_spec_with_processed_validation_to_local_file(
    tmp_path: Path,
):
    input_validations_spec = ValidationsSpec(
        [
            Validation(
                "semantic_model_id",
                "EVALUATE Bla",
                [
                    {"Data[Color]": "Red", "Data[Quantity]": 3},
                    {"Data[Color]": "Red", "Data[Quantity]": 1},
                    {"Data[Color]": "Blue", "Data[Quantity]": 2},
                ],
                True,
                actual_result=[{}, {}],
                state="processed",
                validation_result="passed",
                description="Test",
            )
        ]
    )
    file_path = tmp_path / "validations_spec.json"
    write_validations_spec_to_local_file(input_validations_spec, file_path)
    read_validations_spec = read_validations_spec_from_local_file(file_path)
    assert input_validations_spec == read_validations_spec


def test_local_file_writer_can_write_validations_spec_with_unprocessed_validation_to_local_file_1(
    tmp_path: Path,
):
    input_validations_spec = ValidationsSpec(
        [
            Validation(
                "semantic_model_id",
                "EVALUATE Bla",
                [
                    {"Data[Color]": "Red", "Data[Quantity]": 3},
                    {"Data[Color]": "Red", "Data[Quantity]": 1},
                    {"Data[Color]": "Blue", "Data[Quantity]": 2},
                ],
            )
        ]
    )
    file_path = tmp_path / "validations_spec.json"
    write_validations_spec_to_local_file(input_validations_spec, file_path)
    read_validations_spec = read_validations_spec_from_local_file(file_path)
    assert input_validations_spec == read_validations_spec

from pathlib import Path

import pytest
from click.testing import CliRunner

from pyseval.cli import validate
from pyseval.executor import MirrorExecutor
from pyseval.io import (
    read_validations_spec_from_local_file,
    serialize_validations_spec,
    write_validations_spec_to_local_file,
)
from pyseval.model import Validation, ValidationsSpec


@pytest.fixture()
def validations_spec():
    validation1 = Validation("abc", "abc", [{"Column1": 1, "Column2": 2}])
    validation2 = Validation("abcd", "abcd", [{"Column1": 3, "Column2": 4}])
    validations_spec = ValidationsSpec([validation1, validation2])
    return validations_spec


def test_validate_without_output_option(validations_spec):
    runner = CliRunner()
    with runner.isolated_filesystem() as _:
        file_name = "validations_spec.json"
        write_validations_spec_to_local_file(validations_spec, Path(file_name))
        with open(file_name) as f:
            print(f.readlines())
        result = runner.invoke(
            validate,
            ["-f", file_name, "-e", "mirror"],
        )
        processed_validations_spec = validations_spec.process(MirrorExecutor())
        serialized_processed_validations_spec = serialize_validations_spec(
            processed_validations_spec
        )
        assert result.output == f"{serialized_processed_validations_spec}\n"


def test_validate_with_output_option_as_flag(validations_spec):
    runner = CliRunner()
    with runner.isolated_filesystem() as _:
        file_name = "validations_spec.json"
        write_validations_spec_to_local_file(validations_spec, Path(file_name))
        runner.invoke(
            validate,
            ["-f", file_name, "-o", "-e", "mirror"],
        )
        result_file_name = "validations_spec.result.json"
        read_validations_spec = read_validations_spec_from_local_file(
            Path(result_file_name)
        )
        processed_validations_spec = validations_spec.process(MirrorExecutor())
        assert read_validations_spec == processed_validations_spec


def test_validate_with_output_option_as_custom_value(validations_spec):
    runner = CliRunner()
    with runner.isolated_filesystem() as _:
        input_file_name = "validations_spec.json"
        write_validations_spec_to_local_file(validations_spec, Path(input_file_name))
        output_file_name = "validations_spec_result123.json"
        runner.invoke(
            validate,
            ["-f", input_file_name, "-o", output_file_name, "-e", "mirror"],
        )
        read_validations_spec = read_validations_spec_from_local_file(
            Path(output_file_name)
        )
        processed_validations_spec = validations_spec.process(MirrorExecutor())
        assert read_validations_spec == processed_validations_spec

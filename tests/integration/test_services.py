from pathlib import Path

from pyseval.io import read_validations_spec_from_local_file
from pyseval.services import (
    process_validations_spec_from_local_file_and_write_result_to_local_file,
)


def test_process_validations_spec_from_local_file_and_write_result_to_local_file(
    tmp_path: Path,
):
    output_file_path = tmp_path / "valid_pyseval_validations_spec1.result.json"
    process_validations_spec_from_local_file_and_write_result_to_local_file(
        Path("tests/validations_spec_test_files/valid_pyseval_validations_spec1.json"),
        output_file_path,
    )
    expected_processed_validations_spec = read_validations_spec_from_local_file(
        Path(
            "tests/validations_spec_test_files/valid_pyseval_validations_spec1.result.json"
        )
    )
    actual_processed_validation_spec = read_validations_spec_from_local_file(
        output_file_path
    )
    assert expected_processed_validations_spec == actual_processed_validation_spec

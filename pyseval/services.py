from pathlib import Path

from pyseval.executor import PBIServiceExecutor
from pyseval.io import (
    read_validations_spec_from_local_file,
    serialize_validations_spec,
    write_validations_spec_to_local_file,
)


def process_validations_spec_from_local_file_and_return_resulting_validations_spec(
    input_file_path: Path, executor=PBIServiceExecutor()
) -> str:
    unprocessed_validations_spec = read_validations_spec_from_local_file(
        input_file_path
    )
    processed_validations_spec = unprocessed_validations_spec.process(executor)
    serialized_processed_validations_spec = serialize_validations_spec(
        processed_validations_spec
    )
    return serialized_processed_validations_spec


def process_validations_spec_from_local_file_and_write_result_to_local_file(
    input_file_path: Path, output_file_path: Path, executor=PBIServiceExecutor()
) -> None:
    unprocessed_validations_spec = read_validations_spec_from_local_file(
        input_file_path
    )
    processed_validations_spec = unprocessed_validations_spec.process(executor)
    write_validations_spec_to_local_file(processed_validations_spec, output_file_path)

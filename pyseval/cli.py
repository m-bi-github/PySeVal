from pathlib import Path

import click

from pyseval.executor import EXECUTORS
from pyseval.services import (
    process_validations_spec_from_local_file_and_return_resulting_validations_spec,
    process_validations_spec_from_local_file_and_write_result_to_local_file,
)


@click.command()
@click.option(
    "-f",
    "--file",
    "input_file_path",
    type=click.Path(path_type=Path, exists=True),
    required=True,
    help="the filepath to the validations spec json file",
)
@click.option(
    "-o",
    "--output",
    "output_file_path",
    is_flag=False,
    flag_value="flag",
    type=click.Path(path_type=Path),
    help="the filepath where the validation results should be written to; can be used as a flag in which case the results are written to the input file name as provided in the -f option appended by .result.json; if omitted the result will be written to stdout",
)
@click.option("-e", "--executor", "executor", default="pbiservice", hidden=True)
def validate(input_file_path: Path, output_file_path: Path, executor):
    """validates power bi semantic models from a validations spec json file"""
    executor = EXECUTORS[executor]
    if output_file_path:
        if output_file_path == Path("flag"):
            output_file_path = input_file_path.with_name(
                input_file_path.stem + ".result.json"
            )
        process_validations_spec_from_local_file_and_write_result_to_local_file(
            input_file_path, output_file_path, executor
        )
    else:
        processed_validations_spec = process_validations_spec_from_local_file_and_return_resulting_validations_spec(
            input_file_path, executor
        )
        click.echo(processed_validations_spec)


@click.group()
def cli():
    pass


cli.add_command(validate)

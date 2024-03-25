import json
from pathlib import Path

import jsonschema
import requests

from pyseval import config
from pyseval.model import Validation, ValidationsSpec


def validate_against_json_schema(json: dict) -> None:
    response = requests.get(config.JSON_SCHEMA_URL)
    json_schema = response.json()
    jsonschema.validate(json, json_schema)


def parse_validations_spec(file_content: dict) -> ValidationsSpec:
    validations = []
    for validation in file_content["validations"]:
        validations.append(Validation(**validation))
    return ValidationsSpec(validations)


def read_validations_spec_from_local_file(file_path: Path) -> ValidationsSpec:
    with open(file_path) as f:
        file_content = json.load(f)
    validate_against_json_schema(file_content)
    validations_spec = parse_validations_spec(file_content)
    return validations_spec


def serialize_validations_spec(validations_spec: ValidationsSpec) -> str:
    validations_spec_as_json_string = json.dumps(
        validations_spec, default=lambda x: x.__dict__
    )
    validations_spec_as_dict = json.loads(validations_spec_as_json_string)
    validate_against_json_schema(validations_spec_as_dict)
    return validations_spec_as_json_string


def write_validations_spec_to_local_file(
    validations_spec: ValidationsSpec, file_path: Path
) -> None:
    validations_spec_as_json_string = serialize_validations_spec(validations_spec)
    with open(file_path, "w") as f:
        f.write(validations_spec_as_json_string)

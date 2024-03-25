from pyseval.model import Validation, ValidationsSpec


def test_validations_spec_can_iterate_over_its_validations():
    validations = [
        Validation("abc", "EVALUATE Data", []),
        Validation("abcd", "EVALUATE Data", []),
        Validation("abcde", "EVALUTE Data", [], active=False),
    ]
    validations_spec = ValidationsSpec(validations)
    validations_in_validations_spec = [validation for validation in validations_spec]
    assert validations == validations_in_validations_spec
    assert validations[:-1] == [
        validation for validation in validations_spec if validation.active
    ]

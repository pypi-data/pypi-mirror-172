import uuid

from abf import AbstractExecutionerParameterValidation, AbstractParameterValidation


class SimulatedParamValidation(AbstractParameterValidation):
    str_key: str
    int_key: int
    uuid_key: uuid.UUID


def test_abstract_param_validation_success():
    uuid_value = uuid.uuid4()
    instance = SimulatedParamValidation(str_key="hi", int_key=1, uuid_key=uuid_value)
    serialized_dict = instance.to_serializable_dict()
    assert len(serialized_dict)
    assert serialized_dict.get("uuid_key") == str(uuid_value)


def test_abstract_executioner_param_validation_success():
    uuid_value = uuid.uuid4()
    instance = AbstractExecutionerParameterValidation(
        asset_id=uuid_value, environment_id=uuid.uuid4(), aws_region="us-east-1"
    )
    serialized_dict = instance.to_serializable_dict()
    assert serialized_dict.get("asset_id") == str(uuid_value)

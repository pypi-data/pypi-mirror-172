from typing import Any, Dict

from pydantic import BaseModel

from abf import AbstractAction


class MockUserParameters(BaseModel):
    parameter1: str = "test"


class MockExecutionerParameters(MockUserParameters):
    asset_id: str = "test"


class MockAction(AbstractAction):
    @property
    def user_parameter_model_class(self):
        return MockUserParameters

    @property
    def executioner_parameter_model_class(self):
        return MockExecutionerParameters

    def run_action(self, parameters: Dict[str, Any]):
        return True


def test_validate_user_parameters():
    action = MockAction()
    assert action.validate_user_parameters({"parameter1": "testing"}) == True
    assert not action.validate_user_parameters({"parameter1": False}) == False


def test_user_parameters_property():
    action = MockAction()
    assert action.user_parameter_model_class == MockUserParameters


def test_executioner_parameters_property():
    action = MockAction()
    assert action.executioner_parameter_model_class == MockExecutionerParameters


def test_run_action():
    action = MockAction()
    assert action.run_action({}) == True


def test_get_metadata():
    action = MockAction()
    metadata = action.get_metadata()
    assert "name" in metadata
    assert "description" in metadata
    assert "user_parameters" in metadata
    assert "executioner_parameters" in metadata
    assert metadata["name"] == "mock_action"
    assert metadata["user_parameters"] == MockUserParameters
    assert metadata["executioner_parameters"] == MockExecutionerParameters

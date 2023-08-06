from typing import Tuple
from unittest.mock import MagicMock

from pytest import raises
from terrapyst import TerraformChange

from abf import AbstractPlanValidation


class SimulatedPlanValidationClass(AbstractPlanValidation):
    tf_acceptable_actions: list[str] = ["test-action", "test-action-2", "test-action-3"]
    tf_unacceptable_actions: list[str] = ["test-action-blocked", "test-action-3"]
    tf_types: list[str] = ["test-type"]
    forced_custom_failures: list[str]

    def __init__(self, changes, forced_custom_failures):
        self.changes = changes
        self.forced_custom_failures = forced_custom_failures

    def custom_class_only_validations(self) -> (Tuple[bool, list[str]]):
        """
        simulating failures for the sake of testing, custom plan validations may have their own code
        """
        return len(self.forced_custom_failures) == 0, self.forced_custom_failures

    def validate(self, plan) -> (Tuple[bool, list[str]]):
        failures = []
        # only testing the validator directly without using the plan, typically will have access to plan
        is_acc_allowlist_changes_valid, acc_changes_failures = self.validate_allowlist_tf_changes(
            changes=self.changes, allowlist_changes=self.tf_acceptable_actions, tf_types=self.tf_types
        )
        failures += acc_changes_failures

        is_acc_blocklist_changes_valid, acc_changes_failures = self.validate_blocklist_tf_changes(
            changes=self.changes, blocklist_changes=self.tf_unacceptable_actions, tf_types=self.tf_types
        )
        failures += acc_changes_failures

        is_custom_class_valid, simulated_failures = self.custom_class_only_validations()
        failures += simulated_failures

        return all([is_acc_allowlist_changes_valid, is_acc_blocklist_changes_valid, is_custom_class_valid]), failures


def test_abstract_plan_validation_success() -> None:
    instance = SimulatedPlanValidationClass(
        {
            "1": TerraformChange(
                changeset={"address": "address-1", "type": "test-type", "change": {"actions": ["test-action"]}}
            ),
            "2": TerraformChange(
                changeset={"address": "address-2", "type": "test-type", "change": {"actions": ["test-action-2"]}}
            ),
        },
        [],
    )
    is_valid, failures = instance.validate(MagicMock())
    assert is_valid
    assert not len(failures)


def test_abstract_plan_validation_failure_from_allowlist_changes_checks() -> None:
    instance = SimulatedPlanValidationClass(
        {
            # will fail
            "1": TerraformChange(
                changeset={"address": "address-1", "type": "test-type", "change": {"actions": ["will-fail-action"]}}
            ),
            # will pass
            "2": TerraformChange(changeset={"address": "address-2", "type": "empty", "change": {"actions": []}}),
        },
        [],
    )
    is_valid, failures = instance.validate(MagicMock())
    assert not is_valid
    assert len(failures) == 1


def test_abstract_plan_validation_failure_from_blocklist_changes_only_checks() -> None:
    instance = SimulatedPlanValidationClass(
        {
            # will pass
            "1": TerraformChange(
                changeset={"address": "address-1", "type": "test-type", "change": {"actions": ["test-action"]}}
            ),
            # will fail once - only on blocklist
            "2": TerraformChange(
                changeset={"address": "address-2", "type": "test-type", "change": {"actions": ["test-action-3"]}}
            ),
        },
        [],
    )
    is_valid, failures = instance.validate(MagicMock())
    print(is_valid, failures)
    assert not is_valid
    assert len(failures) == 1


def test_abstract_plan_validation_failure_from_blocklist_and_allowlist_changes_checks() -> None:
    instance = SimulatedPlanValidationClass(
        {
            # will pass
            "1": TerraformChange(
                changeset={"address": "address-1", "type": "test-type", "change": {"actions": ["test-action"]}}
            ),
            # will fail twice (once on allow list, once on blocklist)
            "2": TerraformChange(
                changeset={"address": "address-2", "type": "test-type", "change": {"actions": ["test-action-blocked"]}}
            ),
        },
        [],
    )
    is_valid, failures = instance.validate(MagicMock())
    print(is_valid, failures)
    assert not is_valid
    assert len(failures) == 2


def test_abstract_plan_validation_failure_from_custom_checks() -> None:
    instance = SimulatedPlanValidationClass({}, ["forced_failure"])
    is_valid, failures = instance.validate(MagicMock())
    assert not is_valid
    assert len(failures)


def test_abstract_plan_validation_forcing_format() -> None:
    with raises(TypeError) as exception_info:

        class PlanThatShouldNotConstruct(AbstractPlanValidation):  # NOQA
            pass

        # - ignoring intentionally because this will fail
        PlanThatShouldNotConstruct()  # type: ignore
    assert "Can't instantiate abstract class" in str(exception_info.value)

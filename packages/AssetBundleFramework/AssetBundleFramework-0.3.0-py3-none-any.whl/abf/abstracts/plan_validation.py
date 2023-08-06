from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from terrapyst import TerraformChange, TerraformPlan

PlanTFChanges = Dict[str, TerraformChange]


class AbstractPlanValidation(ABC):
    @abstractmethod
    def validate(self, plan: TerraformPlan) -> Tuple[bool, list[str]]:
        """
        Validates a given plan based on helper classes. This must be implemented but HOW is up to the validator.
        :param plan: TerraformPlan to validates
        :return: returns a bool if valid or not
        """
        raise NotImplementedError

    # Below contains helper validation methods that may be reused

    @staticmethod
    def _validate_changes(
        changes: PlanTFChanges,
        tf_actions: List[str],
        tf_types: List[str],
        is_allowlist: bool,
    ) -> Tuple[bool, List[str]]:
        failed_validations: list[str] = []
        found_failure = False
        for change_key, change in changes.items():
            if change.type in tf_types:
                for action in change.actions:
                    if action not in tf_actions and is_allowlist:
                        # if allowlist based, it only allows things on the allowlist, so if anything else found - error!
                        found_failure = True
                        failed_validations.append(
                            f"allowlist action {action} on {change.type} " f"found in _validate_changes"
                        )
                    elif action in tf_actions and not is_allowlist:
                        # if blocklist based and action is found, error!
                        found_failure = True
                        failed_validations.append(
                            f"blocklist action {action} on {change.type} " f"found in _validate_changes"
                        )
        return not found_failure, failed_validations

    @classmethod
    def validate_blocklist_tf_changes(
        cls, changes: PlanTFChanges, blocklist_changes: List[str], tf_types: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        validates a list of unacceptable actions on a list of types. if at any point an action not in the block list is
        passed in, it will fail
        :param changes: a dictionary of TerraformChanges with the keys being addresses
        :param blocklist_changes: acceptable changes to conduct (ex: "no-op")
        :param tf_types: types that this can be acted on (ex: "aws_internet_gateway")
        :return:
        """
        return cls._validate_changes(changes, blocklist_changes, tf_types, False)

    @classmethod
    def validate_allowlist_tf_changes(
        cls, changes: PlanTFChanges, allowlist_changes: List[str], tf_types: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        validates a list of acceptable actions on a list of types. if at any point an action not in the allowlist is
        passed, it will fail
        :param changes: a dictionary of TerraformChanges with the keys being addresses
        :param allowlist_changes: acceptable changes to conduct (ex: "no-op")
        :param tf_types: types that this can be acted on (ex: "aws_internet_gateway")
        :return:
        """
        return cls._validate_changes(changes, allowlist_changes, tf_types, True)

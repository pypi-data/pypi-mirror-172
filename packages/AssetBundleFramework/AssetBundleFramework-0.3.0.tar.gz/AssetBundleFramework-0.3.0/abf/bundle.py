import importlib.util
import os
import shutil
from ast import Dict
from logging import getLogger
from typing import Any, List, Union

from ruamel.yaml import YAML, YAMLError

from abf.abstracts.acceptance_validation import AbstractAcceptanceValidation
from abf.abstracts.action import AbstractAction
from abf.abstracts.param_validation import (
    AbstractExecutionerParameterValidation,
    AbstractParameterValidation,
)
from abf.abstracts.plan_validation import AbstractPlanValidation

from .errors import ABFBadBundle, ABFMissingAction
from .workspace import AssetWorkspace

logger = getLogger(__name__)

# RT is a subset of the safe loader.
yaml = YAML(typ="rt")


class AssetBundle:
    def __init__(self, repository, asset, version, clone_path) -> None:
        self.repository = repository
        self.cloud = self.repository.cloud
        self.asset = asset
        self.version = version
        self.clone_path = clone_path
        # Python path has to be version unique, as the specs get cached by
        # python based off of the name we provide.
        self.python_path = f"{self.cloud}.{self.asset}.{self.version}"
        self.asset_path_in_repository = f"/modules/{self.asset}"
        self.asset_path = f"{self.clone_path}{self.asset_path_in_repository}"

    def get_identifier(self, include_version=True):
        if include_version:
            return f"{self.cloud}/{self.asset}/{str(self.version)}"
        return f"{self.cloud}/{self.asset}"

    def get_metadata(self):
        path = f"{self.asset_path}/bundle/metadata.yaml"
        if not os.path.exists(path):
            raise ABFBadBundle(f"No asset metadata found at {path}")

        actions = {}
        for action_name in self.list_actions():
            action = self.get_action(action_name)
            actions[action_name] = action.get_metadata()

        with open(path, "r") as stream:
            try:
                metadata = yaml.load(stream)
                metadata["identifier"] = self.get_identifier()
                metadata["actions"] = actions
                metadata["user_parameters"] = self.user_parameter_validator.schema()
                metadata["executioner_parameters"] = self.executioner_parameter_validator.schema()

            except YAMLError as exc:
                raise ABFBadBundle(f"No asset metadata found at {path}") from exc
        return metadata

    @property
    def user_parameter_validator(self) -> AbstractParameterValidation:
        path = f"{self.asset_path}/bundle/validators/parameters.py"
        if not os.path.exists(path):
            raise ABFBadBundle(f"No parameter validator found at {path}")
        return load_module_from_path(f"{self.python_path}.parameters", path).ParameterValidation

    @property
    def executioner_parameter_validator(self) -> AbstractExecutionerParameterValidation:
        path = f"{self.asset_path}/bundle/validators/parameters.py"
        if not os.path.exists(path):
            raise ABFBadBundle(f"No parameter validator found at {path}")
        return load_module_from_path(f"{self.python_path}.parameters", path).ExecutionerParameterValidation

    @property
    def acceptance_validator(self) -> Union[None, AbstractAcceptanceValidation]:
        path = f"{self.asset_path}/bundle/validators/acceptance.py"
        if not os.path.exists(path):
            return None

        acceptance_module = load_module_from_path(f"{self.python_path}.acceptance", path)
        if not hasattr(acceptance_module, "AcceptanceValidation"):
            return None

        AcceptanceValidation = acceptance_module.AcceptanceValidation
        if issubclass(AcceptanceValidation, AbstractAcceptanceValidation):
            return AcceptanceValidation

        return None

    @property
    def plan_validator(self) -> AbstractPlanValidation:
        path = f"{self.asset_path}/bundle/validators/plan.py"
        if not os.path.exists(path):
            raise ABFBadBundle(f"No plan validator found at {path}")
        return load_module_from_path(f"{self.python_path}.plan", path).PlanValidation

    def list_actions(self) -> List[str]:
        path = f"{self.asset_path}/bundle/actions"
        if not os.path.exists(path):
            # No actions found
            return []

        actions = []
        for file in next(os.walk(path))[2]:
            if file == "__init__.py":
                continue
            if file.startswith("."):
                continue
            if file.startswith("test"):
                continue
            if not file.endswith(".py"):
                continue

            action_name = os.path.splitext(file)[0]

            try:
                self.get_action(action_name)
            except:
                logger.exception("Failed to load action")
                continue

            actions.append(action_name)

        return actions

    def get_action(self, action_name: str) -> AbstractAction:

        # First attempt to load the module itself.
        path = f"{self.asset_path}/bundle/actions/{action_name}.py"
        if not os.path.exists(path):
            raise ABFMissingAction(f"No action file found at {path}")
        module = load_module_from_path(f"{self.python_path}.actions/${action_name}", path)

        # Next check the module to pull in the action class.
        class_name = snake_to_camel(action_name)
        if not hasattr(module, class_name):
            raise ABFMissingAction(f"No class named {class_name} in file {path}")

        # Create object from class and return it.
        return getattr(module, class_name)()

    def get_fresh_workspace(self, asset_bundles_dir, workspace="/bundle/workspace"):
        # Copy the full repository so sibling modules can be imported. Also specify child path (optionally)
        # to place user in workspace with proper asset bundle directory. If unset, will be at top of repo
        shutil.copytree(self.clone_path, asset_bundles_dir, ignore=shutil.ignore_patterns(".git"), dirs_exist_ok=True)
        return AssetWorkspace(asset_bundles_dir + self.asset_path_in_repository + workspace)

    # @Deprecated
    def get_parameter_validator(self) -> AbstractParameterValidation:
        logger.warning(
            "AssetBundle.get_parameter_validator is deprecated, please use the AssetBundle.user_parameter_validator property."
        )
        return self.user_parameter_validator

    # @Deprecated
    def get_executioner_parameter_validator(self) -> AbstractExecutionerParameterValidation:
        logger.warning(
            "AssetBundle.get_executioner_parameter_validator is deprecated, please use the AssetBundle.executioner_parameter_validator property."
        )
        return self.executioner_parameter_validator

    # @Deprecated
    def get_plan_validator(self) -> AbstractPlanValidation:
        logger.warning(
            "AssetBundle.get_plan_validator is deprecated, please use the AssetBundle.plan_validator property."
        )
        return self.plan_validator


def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    results = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(results)
    return results


def snake_to_camel(string: str) -> str:
    return "".join(word.title() for word in string.split("_"))

import re
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel


class AbstractAction(ABC):
    @property
    @abstractmethod
    def user_parameter_model_class(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def executioner_parameter_model_class(self):
        raise NotImplementedError

    @property
    def description(self):
        return ""

    @property
    def name(self):
        return camel_to_snake(self.__class__.__name__)

    @abstractmethod
    def run_action(self, parameters: Dict[str, Any]):
        raise NotImplementedError

    def get_metadata(self):
        return {
            "name": self.name,
            "description": self.description,
            "user_parameters": self.user_parameter_model_class,
            "executioner_parameters": self.executioner_parameter_model_class,
        }

    def validate_user_parameters(self, parameters: Dict[str, Any]) -> bool:
        try:
            self.get_user_parameter_model(parameters)
            return True
        except:
            return False

    def get_user_parameter_model(self, parameters: Dict[str, Any]) -> BaseModel:
        return self.user_parameter_model_class.parse_obj(parameters)

    def get_executioner_parameter_model(self, parameters: Dict[str, Any]) -> BaseModel:
        return self.executioner_parameter_model_class.parse_obj(parameters)

    def get_user_output(self, output: Any) -> Any:
        return output


def camel_to_snake(string):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()

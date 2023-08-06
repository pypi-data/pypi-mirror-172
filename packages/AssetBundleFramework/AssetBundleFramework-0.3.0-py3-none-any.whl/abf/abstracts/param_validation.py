import uuid
from abc import ABC
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def convert_to_serializable(value: Any):
    if type(value) == uuid.UUID:
        return str(value)
    return value


class AbstractParameterValidation(BaseModel, ABC):
    type: Optional[str]

    # based on this answer - https://github.com/samuelcolvin/pydantic/discussions/2410#discussioncomment-2512271
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.type = self.__class__.__name__

    def to_serializable_dict(self) -> Dict[str, Any]:
        return {key: convert_to_serializable(value) for key, value in self.dict().items()}


class AbstractExecutionerParameterValidation(AbstractParameterValidation, ABC):
    asset_id: uuid.UUID = Field(description="The specific Asset ID for this instance of the asset.")
    environment_id: uuid.UUID = Field(description="The Environment ID for the Environment that the Asset lives in.")
    outgoing_assets: List[uuid.UUID] = Field(
        default=[], description="A list of assets that this asset has an outgoing connection to."
    )
    incoming_assets: List[uuid.UUID] = Field(
        default=[], description="A list of assets that this asset has an incoming connection from."
    )

    # These value lives here temporarily until we make a way for bundles to have their own parent validator.
    # Unless we want tags in our system as well for lookup type stuff?
    aws_region: Optional[str] = Field(default="us-east-1", description="The default region to launch resources in.")
    tags: Optional[Dict[str, str]] = Field(default={}, description="Tags to add to resources created by this bundle.")

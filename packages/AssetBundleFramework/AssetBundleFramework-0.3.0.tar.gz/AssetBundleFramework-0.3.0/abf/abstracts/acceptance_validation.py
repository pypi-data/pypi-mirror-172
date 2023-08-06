from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from terrapyst import TerraformApplyLog, TerraformPlan


class AbstractAcceptanceValidation(ABC):
    def validate(
        self,
        parameters: Any,
        plan: TerraformPlan,
        apply_log: TerraformApplyLog,
    ) -> Tuple[bool, List[str]]:
        return True, []

import json
from logging import getLogger

from terrapyst import TerraformWorkspace

logger = getLogger(__name__)


class AssetWorkspace(TerraformWorkspace):
    def set_backend(self, backend, options):
        # This gets automatically picked up by terraform given the file extension and
        # does not need to be set with `-backend-config=` (or this class' backend_config attribute).
        # If you do this, you will end up with scary errors of (leave errors below for future searches):
        # 'Error: Extraneous JSON object property' ... 'No argument or block type is named "terraform".'
        #
        # As a result, trust that this file will be used properly if you use this setter.

        # Use JSON to configure the Terraform Block
        # https://www.terraform.io/language/syntax/json#terraform-blocks
        backend_config = {
            "terraform": {
                # Note that the second "backend" is a variable. They key name for the options has to be the engine type.
                "backend": {backend: options},
            }
        }

        with open(str(self.cwd) + "/backend.tf.json", "w+") as f:
            json.dump(backend_config, f)

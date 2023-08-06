# ABF - The Asset Bundle Factory

## Setup

### Locally

When running locally, such as for testing, run-

```bash
make clone
```

If you want to pull in the latest versions of the AssetBundler repositories-

```bash
make reclone
```

### Downstream

If you are not running in this repository directly there's a few steps to take.

1. Create a directory.
2. Set the environment variable `BUNDLE_DIRECTORY` to the newly created directory.
3. Do a full clone of the `terraform-aws-core` bundle into that directory.

## Usage

The top level object is a `AssetRepository`.

```python
from abf import AssetRepository
import tempfile

AWSRepo = AssetRepository("aws")

# you can specify a tag (with get_asset_bundle_by_version), ex: v0.4.1
# you can also specify a ref (with get_asset_bundle_by_ref): ex: like "main" branch for development purposes
bundle = AWSRepo.get_asset_bundle_by_version("rds", "0.4.1")
# or
bundle = AWSRepo.get_asset_bundle_by_ref("rds", "main")

# Note these return the classes themselves, not an instance of the class.
ParameterValidationClass = bundle.get_parameter_validator()
PlanValidationClass = bundle.get_plan_validator()
AcceptanceValidationClass = bundle.get_acceptance_validator()

# Temporary directories disappear outside of the context.
# This means all operations have to be enclosed in the with block.
# Use a permanent directory if that is a problem.
with tempfile.TemporaryDirectory() as workdir:
    # Returns a TerraformWorkspace from terrapy. By default it will drop you in an `executioner` workspace
    workspace = bundle.get_fresh_workspace(workdir)

    # Tell the bundle which state backend to use.
    workspace.set_backend("s3", {
        "bucket": "my_state_bucket",
        "key": "my_state_file.state"
        "dynamodb_table": "state_locks"
        "region": "us-east-1",
    })

    workspace.init()
    workspace.plan()
```

### Environment variables

* `ABF_DISABLE_HARDLINKS` - disable hard links on git checkout and skip using the `--local` flag

## FAQ

* On a Mac using docker volumes in a fully dockerized local setup, you may run into this error: 
`Cloning into '/tmp/<TMP DIRECTORY>/aws/v0.18.0'...\nfatal: failed to create link` from a stderr output when ABF is 
running git operations. To fix this, you can disable hardlinks with an environment variable here: 
`ABF_DISABLE_HARDLINKS='true'`
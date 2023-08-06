import json
import tempfile

from abf import AssetRepository

from .settings import TEST_BUNDLE, TEST_REPOSITORY, TEST_VERSION


def test_custom_backend():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    with tempfile.TemporaryDirectory() as workdir:
        workspace = bundle.get_fresh_workspace(workdir)

        workspace.set_backend("s3", {"region": "us-east-1", "bucket": "test_bucket"})

        with open(workspace.cwd + "/backend.tf.json") as f:
            config = json.load(f)
            assert "s3" in config["terraform"]["backend"]
            assert config["terraform"]["backend"]["s3"]["bucket"] == "test_bucket"
            assert config["terraform"]["backend"]["s3"]["region"] == "us-east-1"

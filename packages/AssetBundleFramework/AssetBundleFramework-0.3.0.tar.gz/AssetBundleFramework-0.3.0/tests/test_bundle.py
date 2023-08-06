import tempfile

from terrapyst import TerraformWorkspace

from abf import AbstractAction, AssetRepository

from .settings import TEST_BUNDLE, TEST_REPOSITORY, TEST_VERSION


def test_parameter_validator():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    parameters = bundle.user_parameter_validator
    assert parameters.__name__ == "ParameterValidation"


def test_executioner_parameter_validator():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    parameters = bundle.executioner_parameter_validator
    assert parameters.__name__ == "ExecutionerParameterValidation"


def test_get_metadata():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE)
    parameters = bundle.get_metadata()
    assert "name" in parameters


def test_get_identifier():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    assert bundle.get_identifier() == f"{TEST_REPOSITORY}/{TEST_BUNDLE}/{TEST_VERSION}"
    assert bundle.get_identifier(include_version=False) == f"{TEST_REPOSITORY}/{TEST_BUNDLE}"


def test_fresh_workspace():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    with tempfile.TemporaryDirectory() as workdir:
        workspace = bundle.get_fresh_workspace(workdir)
    assert isinstance(workspace, TerraformWorkspace)


def test_fresh_workspace_with_overloaded_child_path():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    with tempfile.TemporaryDirectory() as workdir:
        workspace = bundle.get_fresh_workspace(workdir, workspace="tests")
    assert isinstance(workspace, TerraformWorkspace)


def test_fresh_workspace_with_branch():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_ref(TEST_BUNDLE, "main")
    with tempfile.TemporaryDirectory() as workdir:
        workspace = bundle.get_fresh_workspace(workdir)
    assert isinstance(workspace, TerraformWorkspace)


def test_fresh_workspace_with_branch_with_overloaded_child_path():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_ref(TEST_BUNDLE, "main")
    with tempfile.TemporaryDirectory() as workdir:
        workspace = bundle.get_fresh_workspace(workdir, workspace="tests")
    assert isinstance(workspace, TerraformWorkspace)


def test_list_actions():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    assert "return_string" in bundle.list_actions()


def test_get_action():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    assert isinstance(bundle.get_action("return_string"), AbstractAction)


def test_get_acceptance_validator():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, TEST_VERSION)
    assert bundle.acceptance_validator


def test_get_acceptance_validator_return_none_for_old():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, "v0.2.0")
    assert bundle.acceptance_validator == None


def test_get_acceptance_validator_return_none_for_missing():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version("simple_no_acceptance", TEST_VERSION)
    assert bundle.acceptance_validator == None

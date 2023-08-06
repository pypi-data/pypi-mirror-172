import semver
from pytest import raises

from abf import AssetBundle, AssetRepository
from abf.errors import ABFBundleVersionNotFoundException, ABFGitRefNotFoundException

from .settings import TEST_BUNDLE, TEST_REPOSITORY, TEST_VERSION


def test_init_repository():
    repo = AssetRepository(TEST_REPOSITORY)
    assert isinstance(repo, AssetRepository)


def test_get_asset_bundle_no_version():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE)
    assert isinstance(bundle, AssetBundle)


def test_failure_get_asset_bundle_invalid_version():
    with raises(ABFBundleVersionNotFoundException) as exception_info:
        repo = AssetRepository(TEST_REPOSITORY)
        repo.get_asset_bundle_by_version(TEST_BUNDLE, "0.0.0")
    assert "Invalid version passed in " in str(exception_info.value)


def test_failure_get_bundle_string_version_major_not_real():
    with raises(ABFBundleVersionNotFoundException) as exception_info:
        repo = AssetRepository(TEST_REPOSITORY)
        repo.get_asset_bundle_by_version(TEST_BUNDLE, "v999999")
    assert "Unable to find version " in str(exception_info.value)


def test_get_asset_bundle_string_version_major():
    repo = AssetRepository("aws")
    bundle = repo.get_asset_bundle_by_version("rds", "v0")
    assert isinstance(bundle, AssetBundle)


def test_get_asset_bundle_string_version_minor():
    repo = AssetRepository("aws")
    bundle = repo.get_asset_bundle_by_version("rds", "v0.23")
    assert bundle.version == "v0.23.10"
    assert isinstance(bundle, AssetBundle)


def test_get_asset_bundle_string_full_version():
    repo = AssetRepository("aws")
    bundle = repo.get_asset_bundle_by_version("rds", "v0.23.10")
    assert bundle.version == "v0.23.10"
    assert isinstance(bundle, AssetBundle)


def test_failure_get_asset_bundle_version_not_found():
    with raises(ABFBundleVersionNotFoundException) as exception_info:
        repo = AssetRepository(TEST_REPOSITORY)
        repo.get_asset_bundle_by_version(TEST_BUNDLE, "v9999999.0.0")
    assert "Unable to find version " in str(exception_info.value)


def test_get_asset_bundle_ref():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_ref(TEST_BUNDLE, "main")
    assert isinstance(bundle, AssetBundle)


def test_get_asset_bundle_ref_failure():
    with raises(ABFGitRefNotFoundException) as exception_info:
        repo = AssetRepository(TEST_REPOSITORY)
        repo.get_asset_bundle_by_ref(TEST_BUNDLE, "this-ref-should-never-exist-with-an-impossible-name")
    assert "Failed to find ref " in str(exception_info.value)


def test_get_asset_bundle_semver_version():
    repo = AssetRepository(TEST_REPOSITORY)
    bundle = repo.get_asset_bundle_by_version(TEST_BUNDLE, semver.VersionInfo.parse(TEST_VERSION[1:]))
    assert isinstance(bundle, AssetBundle)


def test_list_asset_bundles():
    aws_repo = AssetRepository("aws")
    aws_assets = aws_repo.list_assets()

    # This is an internal "non-asset" module.
    assert not "availability zone" in aws_assets

    repo = AssetRepository("null")
    assets = repo.list_assets()

    # This is our first official asset bundle.
    assert f"{TEST_REPOSITORY}/{TEST_BUNDLE}" in assets
    assert "name" in assets[f"{TEST_REPOSITORY}/{TEST_BUNDLE}"]
    assert assets[f"{TEST_REPOSITORY}/{TEST_BUNDLE}"]["identifier"] == f"{TEST_REPOSITORY}/{TEST_BUNDLE}"

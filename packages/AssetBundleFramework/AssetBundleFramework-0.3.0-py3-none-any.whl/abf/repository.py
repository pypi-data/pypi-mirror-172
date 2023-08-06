import os
import shutil
import subprocess
import tempfile
from logging import getLogger
from pathlib import Path
from typing import List

import semver

from .bundle import AssetBundle
from .errors import (
    ABFBundleVersionNotFoundException,
    ABFException,
    ABFGitFoundException,
    ABFGitRefNotFoundException,
)

BUNDLE_WORK_DIR = Path(tempfile.mkdtemp())

logger = getLogger(__name__)


class AssetRepository:
    def __init__(self, cloud) -> None:
        self.cloud = cloud

        default_bundle_directory = Path(__file__).parent.parent.absolute() / "bundles"
        bundle_directory = os.environ.get("BUNDLE_DIRECTORY", default_bundle_directory)
        self.repo_path = f"{bundle_directory}/terraform-{cloud}-core"
        self.git_path = shutil.which("git")
        if not self.git_path:
            raise ABFGitFoundException("No git binary found.")
        self.versions = self._get_versions()

        if len(self.versions) < 1:
            raise ABFException("No valid versions in repository.")

        self.latest = self.versions[-1]

    def _verify_ref(self, ref: str):
        ref_prefix = "refs/heads"
        if ref.startswith("v"):
            ref_prefix = "refs/tags"

        verified = False
        try:
            # this will always fail with a fatal if not found
            verified_refs_results = self._git_run(["show-ref", "--verify", f"{ref_prefix}/{ref}"])
            verified_refs = verified_refs_results.stdout.strip().split("\n")
            verified = len(verified_refs) > 0 and all([ref for ref in verified_refs])  # may contain empty lines
        except:
            logger.warning(f"Unable to find ref: {ref_prefix}/{ref}")
            return verified

        return verified

    def _get_versions(self):
        tag_results = self._git_run(["tag", "-l", "v*"])
        tags = tag_results.stdout.strip().split("\n")
        versions = []
        for tag in tags:
            try:
                version = semver.VersionInfo.parse(tag[1:])
                versions.append(version)
            except:
                logger.debug(f"Unable to parse {tag} as a semantic version")
        versions.sort()
        return versions

    # this function will use a prefix (ex: "v0" or "v0.1" and extract the possible final version based on that prefix)
    def _get_versions_by_major_minor_prefix(self, asset_type: str, version: str) -> List[semver.VersionInfo]:
        major_minor = version.split(".")
        major = major_minor[0].lstrip("v")
        if len(major_minor) == 2:
            minor = major_minor[1]
            applicable_versions = [v for v in self.versions if v.major == int(major) and v.minor == int(minor)]
        else:
            applicable_versions = [v for v in self.versions if v.major == int(major)]
        if not applicable_versions:
            raise ABFBundleVersionNotFoundException(
                f"Unable to find version '{version}' of asset {asset_type} in {self.cloud}"
            )
        return applicable_versions

    def _git_run(self, args, raise_exception_on_failure=False, **kwargs):
        args.insert(0, self.git_path)
        default_kwargs = {
            "cwd": self.repo_path,
            "capture_output": True,
            "encoding": "utf-8",
            "timeout": None,
        }
        pass_kwargs = {**default_kwargs, **kwargs}
        results = subprocess.run(args, **pass_kwargs)

        if raise_exception_on_failure and not results.returncode == 0:
            raise ABFException(f"An error occurred while running command '{' '.join(args)}'", results)

        return results

    def _get_checkout_by_ref(self, ref: str):
        # checks out by tag and/or branch
        # Create parent dir if it doesn't exist.
        cloud_path = BUNDLE_WORK_DIR / self.cloud
        if not os.path.exists(cloud_path):
            os.makedirs(cloud_path)

        # Clone repo of it doesn't exist.
        clone_path = cloud_path / ref
        if not os.path.exists(clone_path):
            git_command_to_exec = ["clone", "-b", ref, "--local", self.repo_path, clone_path]
            if os.getenv("ABF_DISABLE_HARDLINKS") == "true":
                # on mac file systems using docker, you may want to disable hardlinks or you
                # will run into errors: https://aptible.slack.com/archives/C03C2STPTDX/p1659706961399529
                git_command_to_exec = ["clone", "-b", ref, self.repo_path, clone_path]
            results = self._git_run(git_command_to_exec)

            if results.returncode != 0:
                logger.error(f"Unable to clone clone_path ({clone_path}) provided: {results.stderr}")
                raise ABFException("Failed to clone asset bundle version.")

        return clone_path

    def get_latest(self, major=None, minor=None):
        if not major:
            return self.latest
        filtered = [version for version in self.versions if version.major == major]
        if minor:
            filtered = [version for version in self.versions if version.minor == minor]
        sorted(filtered)
        return filtered[-1]

    def get_asset_bundle_by_ref(self, asset_type, ref="main"):
        if ref == "local":
            return AssetBundle(self, asset_type, str(ref), self.repo_path)

        if not self._verify_ref(ref):
            raise ABFGitRefNotFoundException(f"Failed to find ref ({ref})")

        clone_path = self._get_checkout_by_ref(ref)

        return AssetBundle(self, asset_type, str(ref), clone_path)

    def get_asset_bundle_by_version(self, asset_type, version="latest"):
        if isinstance(version, str):
            if version == "local":
                return self.get_asset_bundle_by_ref(asset_type, "local")
            version_for_semver_lib = version.lstrip("v")  # semver library requires "v" prefix to be missing!
            if version == "latest":
                version = self.latest
            elif version.startswith("v") and len(version.split(".")) < 3:
                version = self._get_versions_by_major_minor_prefix(asset_type, version)[-1]
            elif semver.VersionInfo.isvalid(version_for_semver_lib) and version.startswith("v"):
                version = semver.VersionInfo.parse(version_for_semver_lib)
            else:
                # always raise this error if v prefix is not passed in as it is not valid semver
                raise ABFBundleVersionNotFoundException(f"Invalid version passed in '{version}'")

        if version not in self.versions:
            raise ABFBundleVersionNotFoundException(
                f"Unable to find version '{version}' of asset {asset_type} in {self.cloud}"
            )

        tag = f"v{str(version)}"
        logger.debug(f"Using asset version {tag} for {asset_type}")
        try:
            return self.get_asset_bundle_by_ref(asset_type, tag)
        except Exception as e:
            raise ABFBundleVersionNotFoundException from e

    def list_assets(self, local=False):
        potential_assets = next(os.walk(self.repo_path + "/modules/"))[1]
        assets = {}
        for potential_asset in potential_assets:
            try:
                if local:
                    asset = self.get_asset_bundle_by_version(potential_asset, "local")
                else:
                    asset = self.get_asset_bundle_by_version(potential_asset)
                # If not a real bundle this will raise an exception.
                asset_metadata = asset.get_metadata()
                asset_metadata["identifier"] = asset.get_identifier(include_version=False)
                assets[asset_metadata["identifier"]] = asset_metadata
            except:
                # This just means the module isn't a bundle, so we can ignore it.
                pass

        return assets

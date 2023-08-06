import os
import pathlib

import typer
from ruamel.yaml import YAML

from abf.repository import AssetRepository

if "BUNDLE_DIRECTORY" not in os.environ:
    os.environ["BUNDLE_DIRECTORY"] = str(pathlib.Path.cwd().parent)

# RT is a subset of the safe loader.
yaml = YAML(typ="rt")

app = typer.Typer()


@app.command()
def list(cloud: str):
    repo = AssetRepository(cloud)
    for key in repo.list_assets(local=True):
        typer.echo(key.replace(f"{cloud}/", ""))


@app.command()
def asset_details(cloud: str, asset_name: str):
    repo = AssetRepository(cloud)
    assets = repo.list_assets(local=True)
    typer.echo(yaml.dump(assets[f"{cloud}/{asset_name}"]))


if __name__ == "__main__":
    app()

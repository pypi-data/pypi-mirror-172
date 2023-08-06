import yaml
from typing import Optional
import typer
from os import getcwd
from os.path import basename
import subprocess
from jif.versionbump import VersionBump
from enum import Enum

app = typer.Typer()


def write_jif_yaml(file_content):
    with open("jif.yml", "w") as f:
        yaml.dump(file_content, f, default_flow_style=False, sort_keys=False)
        f.close()


def get_jif_yaml():
    with open("jif.yml", "r") as f:
        file_content = yaml.load(f.read(), Loader=yaml.FullLoader)
        f.close()
        return file_content


@app.command()
def init(
    name: str = typer.Option(
        lambda: basename(getcwd()).replace("-", "_"),
        "--name",
        "-n",
        help="Project name",
        show_default=False,
        prompt=True,
    ),
    version: str = typer.Option(
        "0.0.1", "--version", "-v", help="Current version of project", prompt=True
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
        help="Description of project",
        show_default=False,
        prompt=True,
    ),
):
    write_jif_yaml({"name": name, "version": version, "description": description})
    typer.secho("jif.yml created!", fg=typer.colors.GREEN)


@app.command()
def run(
    script_name: Optional[str] = typer.Argument(None, help="Name of the script to run")
):
    jy = get_jif_yaml()
    scripts = jy.get("scripts")

    if not scripts:
        typer.secho("No scripts exist")
        typer.Exit()

    if script_name:
        script = scripts.get(script_name)
        if script:
            if isinstance(script, str):
                subprocess.call(script.split(" "))
            elif isinstance(script, list):
                for line in script:
                    subprocess.call(line.split(" "))
        else:
            typer.secho(f"{script_name} script does not exist", fg=typer.colors.RED)
        typer.Exit()

    for script in scripts:
        typer.echo(f"{script}:\n  {scripts[script]}")


class BumpTypes(str, Enum):
    major = "major"
    minor = "minor"
    patch = "patch"


@app.command()
def version(
    bump_type: Optional[BumpTypes] = typer.Argument(
        None, autocompletion=lambda: ["major", "minor", "patch"]
    )
):
    jy = get_jif_yaml()
    cur_version = jy.get("version")

    if not cur_version:
        typer.secho("Version missing from jif.yml")
        typer.Exit(1)

    if not bump_type:
        typer.secho(cur_version, fg=typer.colors.CYAN)
        typer.Exit(1)
        return

    vb = VersionBump(cur_version)
    new_version = vb.__getattribute__(bump_type)

    write_jif_yaml({**jy, "version": new_version})


if __name__ == "__main__":
    app()

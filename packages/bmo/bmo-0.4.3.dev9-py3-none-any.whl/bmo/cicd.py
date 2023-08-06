__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import shutil
import typing as T
from pathlib import Path

import yaml

import bmo.common

import typer

app = typer.Typer()


def find_docker():
    return shutil.which("docker")


@app.command("runner")
@app.command("gr")
def run_gitlab_runner(
    command: T.Optional[str] = None,
    jobs: T.List[str] = [],
    pipeline_file: T.Optional[Path] = None,
):
    """Run gitlab-runner"""
    cwd = Path.cwd()
    if pipeline_file is None:
        pipeline_file = cwd / ".gitlab-ci.yml"
    assert (
        pipeline_file.exists()
    ), f"{pipeline_file} doesn't exists. Please use `--pipeline-file`"

    if command is None:
        command = "docker" if find_docker() is not None else "shell"

    with pipeline_file.open("r") as f:
        pipeline_yaml = yaml.safe_load(f)

    if not jobs:
        jobs = list(pipeline_yaml.keys())

    typer.echo("Running following jobs: {','.join(jobs)}")

    output = ""
    docker_options = ""
    docker_sock = Path("/var/run/docker.sock")
    if docker_sock.is_file():
        docker_options = f'--docker-volumes "{docker_sock}:{docker_sock}"'
    for job in jobs:
        if job not in pipeline_yaml:
            available_jobs = list(pipeline_yaml.keys())
            typer.echo(
                f"{job} is not found in pipeline. Available jobs are {available_jobs}"
            )
            continue
        assert shutil.which("gitlab-runner"), "gitlab-runner not found."
        output += bmo.common.run_command(
            f"gitlab-runner exec {command} {docker_options} {job}"
        )
    return output


@app.command("git-semver")
def get_git_semver(metadata: bool = True):
    """Get semver from git-describe. It tries to do the same thing as
    https://github.com/mdomke/git-semver
    """
    git = shutil.which("git")
    assert git, "git is not found"
    output = bmo.common.run_command("git describe --tags", stream=False, silent=True)
    assert output, "Can't determine version string"
    # remove 'v' if any
    o = output.strip().lstrip("v").split("-")
    version = o[0]
    if len(o) > 1:
        try:
            n = int(o[1])
            version += f"-dev.{n}"
        except Exception:
            version += f"-{o[1]}"
    if len(o) > 2 and metadata:
        version += f"+{o[2]}"
    print(version)
    return version


def _test_gitlab_runner():
    out = run_gitlab_runner()
    assert len(out) > 0


def test_cicd():
    _test_gitlab_runner()


if __name__ == "__main__":
    test_cicd()

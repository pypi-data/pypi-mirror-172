# Organization level module.

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import time
import typing as T
import logging

from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def backup(service: str, token: str = "", outdir: T.Optional[Path] = None):
    logging.info(f"backing up {service}")
    if service == "notion":
        from bmo.helpers.notion import Notion

        n = Notion(token)
        try:
            n.backup(outdir)
        except Exception as e:
            logging.warning(f"Failed to create backup because of {e}")
    else:
        raise NotImplementedError(f"{service} is not supported yet")


@app.command()
def monitor_infra(
    infra_file: Path,
    repeat_after_sec: int = 900,
):
    """Monitor a list of url/ip."""
    import bmo.monitor_infra

    # TODO: Check format.
    assert Path(infra_file).exists(), f"{infra_file} does not exist."

    while True:
        bmo.monitor_infra.monitor_infra(infra_file)
        typer.echo(f"Now sleeping for {repeat_after_sec}sec")
        time.sleep(repeat_after_sec)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

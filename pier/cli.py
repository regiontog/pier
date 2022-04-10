import os
import typer

from loguru import logger

from .lib import registry, crane, docker

READONLY_CONFIG = """
version: 0.1
http:
  addr: 0.0.0.0:5000
storage:
  filesystem:
    rootdirectory: /var/lib/registry
maintainance:
  readonly:
    enabled: true
  uploadpurging:
    enabled: false
"""

PULL_THROUGH_CONFIG = """
version: 0.1
http:
  addr: 0.0.0.0:5000
storage:
  filesystem:
    rootdirectory: /var/lib/registry
proxy:
  remoteurl: https://registry-1.docker.io
"""

app = typer.Typer()

@app.command()
def serve(
    cache_dir: str = typer.Option(".pier-cache", "--cache-dir", help="Cache directory"),
):
    logger.info("Starting registry from cache directory {cache_dir}", cache_dir=cache_dir)

    reg, container = registry.start(cache_dir, READONLY_CONFIG, readonly=True)
    logger.info("Registry listening on {reg}", reg=reg)
    docker.logs(container, follow=True)

@app.command()
def mirror(
    mirror_images: str = typer.Argument("-", help="Images to mirror, separated by whitespace"),
    cache_dir: str = typer.Option(".pier-cache", "--cache-dir", help="Cache directory"),
):
    logger.info("Starting mirroring to cache directory {cache_dir}", cache_dir=cache_dir)

    try:
        os.makedirs(cache_dir)
    except:
        pass

    mirror_images = {image for line in typer.open_file(mirror_images) for image in line.split()}

    reg, _ = registry.start(cache_dir, PULL_THROUGH_CONFIG)

    logger.info("Pulling images")

    for image in mirror_images:
        crane.pull(reg, image)

def cli_entrypoint():
    app()
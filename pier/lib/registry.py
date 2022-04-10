import tempfile

from os import path
from time import sleep

from loguru import logger

from . import docker

REGISTRY_IMAGE = "library/registry:2"

def start(cache_dir, config, readonly=False):
    cfg = tempfile.NamedTemporaryFile(mode="w")
    cfg.write(config)
    cfg.flush()

    logger.info("Launching registry")

    registry = docker.detach(REGISTRY_IMAGE, [
        "-P",
        "-v", f"{cfg.name}:/etc/docker/registry/config.yml",
        "-v", f"{path.abspath(cache_dir)}:/var/lib/registry" + (":ro" if readonly else ""),
    ])

    logger.info("Waiting for registry to listen")

    while True:
        if b"listening" in docker.logs(registry):
            break

        sleep(0.2)

    registry_port = docker.inspect(registry,
        format="{{ (index (index .NetworkSettings.Ports \"5000/tcp\") 0).HostPort }}"
    ).decode('utf-8').strip()

    logger.debug("Registry listening on port {registry_port}", registry_port=registry_port)

    return f"localhost:{registry_port}", registry
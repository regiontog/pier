import atexit

from loguru import logger

from . import process

DOCKER_CMD = ["sudo", "docker"]

docker_started_containers = []
atexit.register(lambda: [kill(c) for c in docker_started_containers])


def detach(image, args):
    logger.debug("Launching and detaching from {image}, extra args: {args}", image=image, args=args)
    p = process.run([*DOCKER_CMD, "run", "-d", *args, image], capture_output=True)

    container = p.stdout.decode("utf-8").strip()
    docker_started_containers.append(container)

    return container

def logs(ref, follow=False):
    logger.trace("Fetching container logs {ref}", ref=ref)
    p = process.run([*DOCKER_CMD, "logs", ref] + (["-f"] if follow else []), capture_output=True)

    return p.stderr

def inspect(ref, format=None):
    logger.trace("Inspecting {ref}, with format {format}", ref=ref, format=format)
    p = process.run([*DOCKER_CMD, "inspect", ref] + (["-f", format] if format else []), capture_output=True)

    return p.stdout


def kill(ref):
    logger.debug("Killing container {ref}", ref=ref)
    process.run([*DOCKER_CMD, "kill", ref], capture_output=True)
    process.run([*DOCKER_CMD, "rm", ref], capture_output=True)

    docker_started_containers.remove(ref)
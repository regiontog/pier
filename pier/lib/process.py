import subprocess

from loguru import logger


def run(*args, **kwargs):
    process = subprocess.run(*args, **kwargs, check=False)
    logger.trace(process)

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args, process.stdout, process.stderr)

    return process
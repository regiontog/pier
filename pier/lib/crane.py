from loguru import logger

from . import process

def pull(registry, image):
    logger.debug("Pulling {image} from {registry}", image=image, registry=registry)

    process.run(["crane", "pull", f"{registry}/{image}", "/dev/null"], capture_output=True)
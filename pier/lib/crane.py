from functools import lru_cache
from loguru import logger

from . import process

def pull(registry, image):
    logger.debug("Pulling {image} from {registry}", image=image, registry=registry)

    process.run(["crane", "pull", f"{registry}/{image}", "/dev/null"], capture_output=True)

# def list_all_tags(registry, repo):
#     logger.trace("Fetching all tags in repo {registry}/{repo}", repo=repo, registry=registry)

#     ls = process.run(["crane", "ls", f"{registry}/{repo}"], capture_output=True)

#     for tag in ls.stdout.decode("utf-8").splitlines():
#         yield tag.strip()

# def list_all_images(registry):
#     logger.trace("Fetching all repos in registry {registry}", registry=registry)

#     catalog = process.run(["crane", "catalog", registry], capture_output=True)

#     for repo in catalog.stdout.decode("utf-8").splitlines():
#         for tag in list_all_tags(registry, repo.strip()):
#             yield f"{repo.strip()}:{tag}"


# def delete(registry, image):
#     logger.debug("Deleting {image} from {registry}", image=image, registry=registry)

#     process.run(["crane", "delete", f"{registry}/{image}"], capture_output=True)

# @lru_cache
# def digest(registry, image):
#     logger.trace("Fetching digest of {image} from {registry}", image=image, registry=registry)

#     p = process.run(["crane", "digest", f"{registry}/{image}"], capture_output=True)

#     return p.stdout.decode("utf-8").strip()
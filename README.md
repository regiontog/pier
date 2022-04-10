# Pier

Docker image mirroring to disk

# Demo
[![Pier video demo](docs/demo.gif)](https://www.youtube.com/watch?v=HqjznbBxseI)

## How

Uses [library/registry](https://hub.docker.com/_/registry) in pull through mode to efficiently mirror docker images to disk using the filesystem storage driver. Thanks to image layering the total size of the caching directory will be about equal or smaller that the combined compressed size of the images. The time-to-live of the registry blob cache is hardcoded to 7days, solved by MR [#3238](https://github.com/distribution/distribution/pull/3238), so all images that needs to be mirrored should be pulled before a sync/backup to avoid any missing blobs. Any old images not specified in the mirror job might be GC'ed by the registry. So long as the mirroring job is ran more than once every 7 days no unnecessary blobs should be fetched.

## Links
* [library/registry dockerhub](https://hub.docker.com/_/registry)
* [library/registry github](https://github.com/distribution/distribution)
* [registry config](https://docs.docker.com/registry/configuration)
* [pull through documentation](https://docs.docker.com/registry/recipes/mirror)
* [garbage collection documentation](https://github.com/distribution/distribution/blob/main/docs/garbage-collection.md)
* [ttl cache MR](https://github.com/distribution/distribution/pull/3238)

## Usage
### Mirror images to cache
```bash
echo library/alpine:3.14 library/alpine:3:15 | pier mirror --cache-dir my-cache-dir
```

### Serve from cache
```bash
# Starts the registry in read only mode with the cache dir bind mounted in ro mode
pier serve --cache-dir my-cache-dir
```

### Calculate size of images (only images hosted on https://hub.docker.com)
```bash
for i in $(cat images); do;  curl -s https://hub.docker.com/v2/repositories/$(echo $i | cut -d ':' -f1)/tags/$(echo $i | cut -d ':' -f2) | jq -r '.full_size'; done | python -c "import sys; print(sum(int(l) for l in sys.stdin))" | numfmt --to=si
```
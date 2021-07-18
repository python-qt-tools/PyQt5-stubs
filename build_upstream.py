import argparse
import io
import re
import tarfile
from pathlib import Path
import typing

import docker
from docker import DockerClient
from docker.models.images import Image
from docker.utils.json_stream import json_stream

DEFAULT_DOCKERFILE = Path("Dockerfile")
DEFAULT_OUTPUT_DIR = Path("PyQt6-stubs")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build PyQt stubs in Docker")

    # noinspection PyTypeChecker
    parser.add_argument('-d', '--dockerfile', type=Path,
                        default=DEFAULT_DOCKERFILE,
                        help="Dockerfile to build")

    # noinspection PyTypeChecker
    parser.add_argument('-o', '--output-dir', type=Path,
                        default=DEFAULT_OUTPUT_DIR,
                        help="Directory to find package(s) to be built. "
                             "Defaults to ./pkg")

    # noinspection PyTypeChecker
    parser.add_argument('-j', '--jobs', type=int,
                        default=1,
                        help="The number of jobs to launch in parallel. "
                             "Defaults to 1")

    # noinspection PyTypeChecker
    parser.add_argument('--no-cache',
                        action='store_true',
                        help="Do not use Docker caches. Defaults to false")

    return parser.parse_args()


def main():
    args = parse_args()

    docker_client = docker.from_env()

    image_id = build_image(docker_client, args.dockerfile, args.jobs, args.no_cache)

    extract_output(docker_client, image_id, args.output_dir)


def build_image(docker_client: DockerClient, dockerfile: Path, jobs: int, no_cache: bool) -> str:
    image_name = "pyqt5-stubs"

    # Using low-level API so that we can log as it occurs instead of only
    # after build has finished/failed
    resp = docker_client.api.build(
        path=str(dockerfile.parent),
        rm=True,
        tag=image_name,
        buildargs={"MAKEFLAGS": f"-j{jobs}"},
        nocache=no_cache)

    image_id: str = typing.cast(str, None)
    for chunk in json_stream(resp):
        if 'error' in chunk:
            message = f"Error while building Dockerfile for " \
                      f"{image_name}:\n{chunk['error']}"
            print(message)
            raise DockerBuildError(message)

        elif 'stream' in chunk:
            print(chunk['stream'].rstrip('\n'))
            # Taken from the high level API implementation of build
            match = re.search(r'(^Successfully built |sha256:)([0-9a-f]+)$',
                              chunk['stream'])
            if match:
                image_id = match.group(2)

    if not image_id:
        message = f"Unknown Error while building Dockerfile for " \
                  f"{image_name}. Build did not return an image ID"
        raise DockerBuildError(message)

    return image_id


def extract_output(docker_client: DockerClient, image_id: str,
                   output_dir: Path) -> None:
    image = docker_client.images.get(image_id)
    container = docker_client.containers.create(image)

    # Get archive tar bytes from the container as a sequence of bytes
    package_tar_byte_gen: typing.Generator[bytes, None, None]
    package_tar_byte_gen, _ = container.get_archive("/output/",
                                                    chunk_size=None)

    # Concat all the chunks together
    package_tar_bytes: bytes
    package_tar_bytes = b"".join(package_tar_byte_gen)

    # Create a tarfile from the tar bytes
    tar_file_object = io.BytesIO(package_tar_bytes)
    package_tar = tarfile.open(fileobj=tar_file_object)

    # Extract the files from the tarfile to the disk
    for tar_deb_info in package_tar.getmembers():
        # Ignore directories
        if not tar_deb_info.isfile():
            continue

        # Directory that will contain the output files
        output_dir.mkdir(parents=True, exist_ok=True)

        # Filename (without outer directory)
        tar_deb_info.name = Path(tar_deb_info.name).name

        # Extract
        package_tar.extract(tar_deb_info, output_dir)


class DockerBuildError(RuntimeError):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    main()

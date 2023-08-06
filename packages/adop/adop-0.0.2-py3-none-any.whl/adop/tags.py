import configparser
import pathlib
import re

from . import exceptions


def store(
    root_dir_name: str,
    cache_hash: str,
    tag: str,
    cache_root: str,
):
    """
    Generate or update a tags file (ini format) that maps a tag with a sha256sum
    """

    config, config_file_path = get_config(cache_root)
    if not config.has_section(root_dir_name):
        config.add_section(root_dir_name)
    config.set(root_dir_name, tag, cache_hash)
    with config_file_path.open(mode="w") as f:
        config.write(f)


def get_config(
    cache_root: str,
) -> "tuple[~configparser.ConfigParser, ~pathlib.Path]":
    """
    Returns the path and contents of ``tags.ini``.

    :return:
        - A `tuple` of:
            - config object (`~configparser.ConfigParser`)
            - ``config_file_path`` (`~pathlib.Path`)
    """
    tags_root = pathlib.Path.cwd().joinpath(cache_root)
    tags_root.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config_file_path = tags_root.joinpath("tags.ini")
    if config_file_path.exists():
        config.read_string(config_file_path.read_text())
    return config, config_file_path


def find_shasum_from_headers(cache_root: str, root: str, headers: dict) -> str:
    """
    Find a pre stored sha256sum using the Zip-Tag header from request object

    :return: The sha256sum of the file.
    """

    tag = headers.get("Zip-Tag", "")
    if not tag:
        raise exceptions.Fail("header Zip-Tag is missing")
    if not re.search(r"[^\w\.-]", tag) is None:
        raise exceptions.Fail("header Zip-Tag is not a valid tag.")
    if len(tag) >= 64:
        raise exceptions.Fail("header Zip-Tag to long")

    config, config_file_path = get_config(cache_root)
    if not config.has_section(root):
        raise exceptions.CacheNotFound(f"Zip-Tag not found: {tag}")
    if not config.has_option(root, tag):
        raise exceptions.CacheNotFound(f"Zip-Tag not found: {tag}")

    sha256sum = config.get(root, tag)
    if not sha256sum:
        raise exceptions.CacheNotFound(f"Zip-Tag not found: {tag}")

    return sha256sum

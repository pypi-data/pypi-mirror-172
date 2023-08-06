import json
import pathlib


def get_dict(cache_root: str, root: str) -> "dict[str, dict]":
    """
    Returns a dict with info of the current cache
    """
    mapping = {}
    file_list = pathlib.Path(cache_root).glob("*/post_metadata.json")
    for file in file_list:
        info = json.loads(file.read_text())
        root_from_url = ""
        if "root" in info:
            root_from_url = info["root"]
        if "root_from_url" in info:
            root_from_url = info["root_from_url"]

        if root and not root == root_from_url:
            continue

        if root_from_url:
            if root_from_url not in mapping:
                mapping[root_from_url] = {}
            mapping[root_from_url][file.parent.stem] = {
                "sha256": info.get("sha256", ""),
                "tag": info.get("tag", ""),
                "serial": info.get("serial", 0),
            }

    return mapping

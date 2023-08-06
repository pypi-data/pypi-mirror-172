import json
import os

from . import (
    exceptions,
    parse_config,
    store_payload,
    unpack_payload,
    uploaders,
    zip_install,
)


def upload(file: str, config: str, cwd: str, remote: str, install: str, deploy: bool):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, "", "")

    uploader = Uploader(local_config)

    requires_file_data = uploader.parse_requires_file(file)
    install_data = uploader.parse_install_to(install, requires_file_data)
    remote_data = uploader.parse_remotes(remote, requires_file_data)

    requires_data = requires_file_data["requires"]
    uploader.upload(install_data, remote_data, requires_data, deploy)


class Uploader(zip_install.RequireFile):
    def upload(
        self, install_data: dict, remote_data: dict, requires_data: dict, deploy: bool
    ):

        _handle_zip = self.gen(install_data, remote_data, requires_data, deploy)

        try:
            for res in _handle_zip:
                if isinstance(res, dict):
                    if "root" in res:
                        print(f"Requires: {res['root']}")
                    elif "result" in res:
                        print(f"{json.dumps(res)}")
                else:
                    print(f"          {res}")
        except exceptions.CommandFail as err:
            print("          ERROR:")
            raise exceptions.CommandFail(f"             {err}")

    def gen(
        self, install_data: dict, remote_data: dict, requires_data: dict, deploy: bool
    ):
        cache_root = install_data["cache_root"]

        for root, shasum in requires_data.items():
            yield {"root": root}  # first result: returns only root
            yield f"checking {root}={shasum[:15]}..."

            if shasum.startswith("tag:"):
                headers = {"Zip-Tag": shasum.split(":", 1)[1].strip()}
            elif shasum.startswith("sha256:"):
                headers = {"Zip-Sha256": shasum.split(":", 1)[1].strip()}
            else:
                raise exceptions.CommandFail(
                    "Only sha256 is supported in the [requires] section. "
                    f"ie. {root} = sha256:AABBCC"
                )

            yield f"using cache_root: {cache_root}"
            try:
                cache_file, *_ = store_payload.find_file_from_headers(
                    cache_root, root, headers
                )
            except exceptions.Fail as err:
                raise exceptions.CommandFail(err)
            zip_root = unpack_payload.extract_root_dir_name(cache_file)
            headers["Zip-Root"] = zip_root
            yield from uploaders.api_upload(
                cache_file, root, remote_data, headers, deploy
            )

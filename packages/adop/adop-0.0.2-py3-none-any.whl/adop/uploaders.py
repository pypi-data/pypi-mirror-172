import json
import pathlib
import ssl
from urllib import error, request

from . import exceptions


def api_upload(
    cache_file: pathlib.Path, root: str, remote_data: dict, headers: dict, deploy: bool
):
    try:
        yield from simple_api_uploader(cache_file, root, remote_data, headers, deploy)
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {root}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{err}")


def simple_api_uploader(
    cache_file: pathlib.Path, root: str, remote_data: dict, headers: dict, deploy: bool
):
    """
    A simple uploader. No resume-support. Will not handle transfer errors.

    Yield protocol:
    - str: log
    - dict: progress

    This is a generator that returns a tuple. You have to call it with ``yield from``
    to receive the return value.

    .. code-block:: pycon

        >>> def gen():
        ...   yield from simple_api_uploader(cache_file, remote_data, root, headers)

        >>> for res in gen()
        ...     print(res)

    :returns: A generator
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)

    if deploy:
        endpoint = f"{prefix}/deploy/zip/{root}"
    else:
        endpoint = f"{prefix}/upload/zip/{root}"

    headers["Token"] = token
    req = request.Request(url=endpoint, headers=headers, data=cache_file.read_bytes())

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield {"progress": 0}
    yield f"uploading {root}"
    res = request.urlopen(req, context=context)

    buffer = " "
    payload = ""
    yield f"response from {prefix}"
    while buffer:
        buffer = res.readline(1024).decode(errors="ignore")
        if buffer.startswith("//"):
            yield f"      {buffer[2:].strip()}"
        else:
            payload += buffer

    if not json.loads(payload)["result_code"] == 0:
        raise exceptions.CommandFail(f"Upload failed: {payload}")

    yield {"progress": 100}
    if deploy:
        yield "upload and deployment complete"
    else:
        yield "upload complete"

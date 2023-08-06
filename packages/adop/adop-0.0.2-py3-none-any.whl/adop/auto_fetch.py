import atexit
import configparser
import logging
import pathlib
from threading import Event, Thread
from urllib import request

from flask import Flask

from . import auto_fetch_state, auto_sequences

logger = logging.getLogger(__name__)


def run_in_background(app: Flask, local_config: configparser.ConfigParser) -> Thread:
    """
    Start the auto fetch worker in a background thread as a daemon and
    returns the thread handle
    """
    auto_fetch_thread = Auto_Fetch_Thread(
        name="auto_fetch_thread", args=(app, local_config), daemon=True
    )
    auto_fetch_thread.start()
    return auto_fetch_thread


class Interrupt(Event):
    """
    Use to exit the background thread or to trigger
    a fetch event.
    """

    def __init__(self):
        super().__init__()
        self.exit = False
        self.fetch = False

    def clear(self):
        self.exit = False
        self.fetch = False
        super().clear()

    def set_fetch(self):
        "Signal the background worker to run the ``auto-fetch`` routine"
        self.fetch = True
        self.set()

    def set_exit(self):
        "Signal the background worker to exit"
        self.exit = True
        self.set()


class Auto_Fetch_Thread(Thread):
    """
    Automatically downloads and unpack zip files from a http source.
    Triggers on interval or `Interrupt.set_fetch`.
    """

    def run(self):
        """
        Background thread loop. Will exit on `Interrupt.set_exit`.
        """
        self.app, self.config = self._args
        interrupt = Interrupt()

        atexit.register(interrupt.set_exit)
        self.app.config["auto_fetch_event"] = interrupt

        auto_fetch_interval = self.config.getint("autofetch", "interval")
        if auto_fetch_interval < 1:
            auto_fetch_interval = None

        interrupt.wait(2)

        if not self.config.getboolean("autofetch", "run_at_startup"):
            interrupt.wait(auto_fetch_interval)

        while not interrupt.exit:

            if interrupt.is_set():
                interrupt.clear()

            sources_config = configparser.ConfigParser()
            sources_config.read_dict({"autofetch": {"sources": ""}})
            sources_path = self.config.get("autofetch", "config")
            if sources_path:
                sources_config.read_string(
                    pathlib.Path.cwd().joinpath(sources_path).read_text()
                )
            cache_root = self.config.get("server", "cache_root")

            self.fetch_updates(cache_root, sources_config)
            interrupt.wait(auto_fetch_interval)

    def check_update(
        self, state: auto_fetch_state.State, src: str, url: request.Request
    ) -> str:
        """
        Returns a new hash if a update is found, and a empty string if not.
        Checks if the given url content is same as previous check
        """
        with request.urlopen(url) as f:
            content = f.read()
        new_state = state.make(content)
        prev_state = state.get(src)
        if not new_state == prev_state:
            return new_state
        return ""

    def fetch_updates(self, cache_root: str, sources_config: configparser.ConfigParser):
        """
        Downloads and unpack zip files from given sources if an update is
        detected.
        """
        logger.info("checking for updates")

        sources = sources_config.get("autofetch", "sources").split(",")
        sources = [src.strip(" ") for src in sources]

        state = auto_fetch_state.State(cache_root)
        has_update = False
        for src_name in sources:
            src = f"autofetch:{src_name}"
            try:
                check_url = sources_config.get(src, "check_url")
                payload_url = sources_config.get(src, "payload_url")
                if sources_config.has_option(src, "headers"):
                    headers = unpack_headers(sources_config.get(src, "headers"))
                else:
                    headers = {}

                root = sources_config.get(src, "root")
                new_state = self.check_update(
                    state, src, request.Request(url=check_url, headers=headers)
                )

                if new_state:
                    logger.info(f"{src_name}: update available")

                    req = RequestInterface(
                        {"Zip-Root": sources_config.get(src, "zip_root", fallback="")},
                        url=request.Request(url=payload_url, headers=headers),
                        remote_addr="",
                        remote_user="",
                    )
                    _handle_zip = auto_sequences.handle_zip(
                        self.app, req, root, store_data=True, unpack_data=True
                    )
                    for res in _handle_zip:
                        if isinstance(res, str):
                            logger.info(f"{src_name}: {res}")
                        elif isinstance(res, dict) and "result_code" in res:
                            logger.info(f"{src_name}: {res}")
                            if res["result_code"] == 0:
                                state.update(src, new_state)
                                has_update = True

            except Exception as err:
                logger.error(f"{src_name}: {repr(err)}")

        if has_update:
            state.store()


def unpack_headers(header_str: str) -> dict:
    """
    Parse string. Format: ``"key1:val1,key2:val2"``

    :return: `dict` format: ``{"key1":"val1", "key2":"val2"}``
    """
    headers = {}
    for header in header_str.split(","):
        k, v = header.split(":", 1)
        headers[k.strip(" ")] = v.strip(" ")
    return headers


class RequestInterface:
    """
    A class interface that can be used as argument in auto_sequences.handle_zip
    instead of the Flask.request object.
    """

    __slots__ = ("headers", "url", "remote_addr", "remote_user")

    def __init__(
        self, headers: dict, url: request.Request, remote_addr: str, remote_user: str
    ):
        self.headers = headers
        self.url = url
        self.remote_addr = remote_addr
        self.remote_user = remote_user

    def get_data(self) -> bytes:
        with request.urlopen(self.url) as f:
            content = f.read()
            info = f.info()
            if "Content-Length" in info:
                self.headers["Content-Length"] = int(info["Content-Length"])
            else:
                self.headers["Content-Length"] = len(content)
        return content

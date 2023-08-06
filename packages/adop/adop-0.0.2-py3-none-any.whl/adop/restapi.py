import json
import logging
import os
from functools import wraps
from threading import Lock

import waitress
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    request,
    send_file,
    stream_with_context,
)
from werkzeug.serving import run_simple

from . import (
    auto_fetch,
    auto_sequences,
    cache_state,
    deploy_state,
    exceptions,
    parse_config,
    store_payload,
    tags,
)

app = Flask(__name__)


def serve(config: str, cwd: str, host: str, port: int):
    """
    Start the webserver and a `~.auto_fetch.Auto_Fetch_Thread` background thread.
    Blocks until :kbd:`ctrl+c`
    is received.
    """
    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))
    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, host, port)

    # enforce authorization token
    if not local_config.get("server", "write_token"):
        raise SystemExit("[server]write_token missing in config file")
    if not local_config.get("server", "read_token"):
        raise SystemExit("[server]read_token missing in config file")

    app.config["deploy_root"] = local_config.get("server", "deploy_root")
    app.config["cache_root"] = local_config.get("server", "cache_root")
    app.config["write_token"] = local_config.get("server", "write_token")
    app.config["read_token"] = local_config.get("server", "read_token")
    app.config["shared_lock"] = Lock()
    app.config["shared_progress_dict"] = {}
    app.config["keep_on_disk"] = 0
    app.config["auto_fetch_event"] = None
    if local_config.getboolean("auto_delete", "on"):
        app.config["keep_on_disk"] = local_config.getint("auto_delete", "keep_on_disk")

    app.logger.info("cwd: %s", os.getcwd())
    app.logger.info("config: %s", abs_conf_path)
    app.logger.info("deploy_root: %s", app.config["deploy_root"])
    app.logger.info("cache_root: %s", app.config["cache_root"])
    app.logger.info("keep_on_disk: %d", app.config["keep_on_disk"])

    host = local_config.get("server", "host")
    port = local_config.getint("server", "port")
    debug = local_config.getint("server", "debug")

    if debug and ".." in cwd:
        raise SystemExit(
            "Error: Cannot combine debug-mode with relative parent paths [..]"
        )

    ssl_on = local_config.getboolean("server", "ssl_on")
    ssl_certificate = local_config.get("server", "ssl_certificate")
    ssl_certificate_key = local_config.get("server", "ssl_certificate_key")

    ssl_context = None
    if ssl_on:
        ssl_context = (ssl_certificate, ssl_certificate_key)

    if local_config.getboolean("autofetch", "on"):
        if not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            auto_fetch.run_in_background(app, local_config)

    if local_config.getboolean("server", "on"):

        if debug == 0:
            if ssl_on:
                run_simple(
                    host,
                    port,
                    app,
                    use_reloader=False,
                    use_debugger=False,
                    threaded=True,
                    ssl_context=ssl_context,
                )
            else:
                waitress_logger = logging.getLogger("waitress")
                waitress_logger.setLevel(logging.INFO)
                waitress.serve(app, host=host, port=port)
        else:
            app.run(debug=True, host=host, port=port, ssl_context=ssl_context)

    app.logger.info("exit")


def require_write_token(f):
    """
    A decorator to check for a valid write-token

    :param function f: A function bound to a URL.

    :return: A function
    """

    @wraps(f)
    def verify_token(*args, **kwargs):
        if not request.headers.get("token") == app.config["write_token"]:
            return make_response(
                jsonify({"result": "Invalid token", "result_code": 4}), 401
            )
        return f(*args, **kwargs)

    return verify_token


def require_read_token(f):
    """
    A decorator to check for a valid token

    :param function f: A function bound to a URL.

    :return: A function
    """

    @wraps(f)
    def verify_token(*args, **kwargs):
        if not request.headers.get("token") in (
            app.config["read_token"],
            app.config["write_token"],
        ):
            return make_response(
                jsonify({"result": "Invalid token", "result_code": 4}), 401
            )
        return f(*args, **kwargs)

    return verify_token


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(result_code=404, result=str(e)), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(result_code=405, result=str(e)), 405


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(result_code=500, result=str(e)), 500


@app.route("/api/v1/test", methods=["GET"])
@require_read_token
def get_test() -> Response:
    "Bound to ``GET /api/v1/test``"
    return jsonify({"result": "It works", "result_code": 0})


@app.route("/api/v1/progress", methods=["GET"])
@require_write_token
def get_progress() -> Response:
    "Bound to ``GET /api/v1/progress``"
    try:
        with app.config["shared_lock"]:
            progress = app.config["shared_progress_dict"].copy()
        progress_as_json = jsonify(progress)
    except Exception as err:
        app.logger.exception(err)
        progress_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return progress_as_json


@app.route("/api/v1/state", methods=["GET"])
@require_read_token
def get_state() -> Response:
    "Bound to ``GET /api/v1/state``"
    try:
        with app.config["shared_lock"]:
            state_config, *_ = deploy_state.get_config(app.config["deploy_root"])
        state = {
            section: state_config[section].get("source_hash")
            for section in state_config.sections()
        }
        state_as_json = jsonify(state)
    except Exception as err:
        app.logger.exception(err)
        state_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return state_as_json


@app.route("/api/v1/state/<root>", methods=["GET"])
@require_read_token
def get_state_item(root: str) -> Response:
    "Bound to ``GET /api/v1/state/<root>``"
    try:
        with app.config["shared_lock"]:
            state_config, *_ = deploy_state.get_config(app.config["deploy_root"])
        state = {root: state_config[root].get("source_hash")}
        state_as_json = jsonify(state)
    except Exception as err:
        app.logger.exception(err)
        state_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return state_as_json


@app.route("/api/v1/tags/<root>", methods=["GET"])
@require_read_token
def get_tags_root(root: str) -> Response:
    "Bound to ``GET /api/v1/tags/<root>``"
    try:
        with app.config["shared_lock"]:
            tags_config, _ = tags.get_config(app.config["cache_root"])
        tags_as_json = jsonify({k: v for k, v in tags_config[root].items()})
    except Exception as err:
        app.logger.exception(err)
        tags_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return tags_as_json


@app.route("/api/v1/tags/<root>/<tag>", methods=["GET"])
@require_read_token
def get_tags_root_tag(root: str, tag: str) -> Response:
    "Bound to ``GET /api/v1/tags/<root>/<tag>``"
    try:
        with app.config["shared_lock"]:
            tags_config, _ = tags.get_config(app.config["cache_root"])
        tags_as_json = jsonify({k: v for k, v in tags_config[root].items() if k == tag})
    except Exception as err:
        app.logger.exception(err)
        tags_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return tags_as_json


@app.route("/api/v1/list/zip", methods=["GET"])
@app.route("/api/v1/list/zip/<root>", methods=["GET"])
@require_read_token
def get_list_zip(root: str = "") -> Response:
    "Bound to ``GET /api/v1/list/zip``"
    try:
        with app.config["shared_lock"]:
            cache_dict = cache_state.get_dict(app.config["cache_root"], root)
        state_as_json = jsonify(cache_dict)
    except Exception as err:
        app.logger.exception(err)
        state_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return state_as_json


@app.route("/api/v1/trigger/fetch", methods=["GET"])
@require_write_token
def trigger_fetch() -> Response:
    "Bound to ``GET /api/v1/trigger/fetch``"
    try:
        with app.config["shared_lock"]:
            auto_fetch_event = app.config["auto_fetch_event"]
        if auto_fetch_event:
            auto_fetch_event.set_fetch()
            res_as_json = jsonify({"result": "OK", "result_code": 0})
        else:
            res_as_json = jsonify(
                {"result": "auto_fetch is not available", "result_code": 1}
            )
    except Exception as err:
        app.logger.exception(err)
        res_as_json = make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )
    return res_as_json


@app.route("/api/v1/download/zip/<root>", methods=["GET"])
@require_read_token
def download_zip(root: str) -> Response:
    "Bound to ``GET /api/v1/download/zip/<root>``"

    try:
        if "Zip-Sha256" in request.headers:
            zip_file, *_ = store_payload.find_file_from_headers(
                app.config["cache_root"], root, request.headers
            )
        elif "Zip-Tag" in request.headers:
            zip_file, *_ = store_payload.find_file_from_headers(
                app.config["cache_root"], root, request.headers
            )
        else:
            with app.config["shared_lock"]:
                state_config, *_ = deploy_state.get_config(app.config["deploy_root"])
                zip_file = state_config[root].get("source_file")
        return send_file(zip_file, as_attachment=True)
    except FileNotFoundError as err:
        return make_response(
            jsonify({"result": f"Internal Error {repr(err)}", "result_code": 5}), 500
        )
    except exceptions.Fail as err:
        return make_response(
            jsonify({"result": f"Internal Error {repr(err)}", "result_code": 5}), 500
        )
    except Exception as err:
        app.logger.exception(err)
        return make_response(
            jsonify({"result": "Internal Error", "result_code": 5}), 500
        )


@app.route("/api/v1/upload/zip/<root>", methods=["POST", "PUT"])
@require_write_token
def upload_zip(root: str) -> Response:
    "Bound to ``POST/PUT /api/v1/upload/zip/<root>``"
    return Response(
        stream_with_context(
            handle_zip_as_stream(root, store_data=True, unpack_data=False)
        ),
        content_type="application/json",
    )


@app.route("/api/v1/deploy/zip/<root>", methods=["POST", "PUT"])
@require_write_token
def post_deploy_zip(root: str) -> Response:
    "Bound to ``POST/PUT /api/v1/deploy/zip/<root>``"
    return Response(
        stream_with_context(
            handle_zip_as_stream(root, store_data=True, unpack_data=True)
        ),
        content_type="application/json",
    )


@app.route("/api/v1/deploy/zip/<root>", methods=["GET"])
@require_write_token
def get_deploy_zip(root: str) -> Response:
    "Bound to ``GET /api/v1/deploy/zip/<root>``"
    return Response(
        stream_with_context(
            handle_zip_as_stream(root, store_data=False, unpack_data=True)
        ),
        content_type="application/json",
    )


def handle_zip_as_stream(root: str, store_data: bool, unpack_data: bool):
    """
    Stream the progress back to client. The result is formatted as json
    but progress and logging data is not valid json. If client ignores
    lines prefixed with ``//`` the result should be valid json

    :return: A generator
    """

    _handle_zip = auto_sequences.handle_zip_in_threadpool(
        app, request.__copy__(), root, store_data, unpack_data
    )

    for res in _handle_zip:
        if isinstance(res, dict):
            if "result" in res:
                yield f"{json.dumps(res)}\n"
        else:
            yield f"// {res}\n"

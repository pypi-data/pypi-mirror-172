import configparser
import os
import pathlib
import secrets

from . import exceptions, hooks

default_config = """[server]
on = 1
host = 127.0.0.1
port = 8000
debug = 0

ssl_on = 0
ssl_certificate =
ssl_certificate_key =

deploy_root = ./work/auto
cache_root = ./work/cache

write_token =
read_token = ${write_token}

[auto_delete]
on = 1
keep_on_disk = 5

[autofetch]
on = 0
run_at_startup = 1
interval = 7200
sources =
config =

[client]
install = basedir
remote = local

[remote:local]
url = http://${server:host}:${server:port}/api/v1
token = ${server:write_token}
insecure = 0

[install:homedir]
install_root = ~/.adop-autolibs-cache/autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:basedir]
install_root = ./autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:parentdir]
install_root = ../autolibs
cache_root = ~/.adop-autolibs-cache/cache

[install:subprojdir]
install_root =  ~/.adop-autolibs-cache/autolibs
cache_root = ~/.adop-autolibs-cache/cache
hook:transform-root = builtins:basedir:add-as-prefix
"""

default_example_config = """
[autofetch]
sources = github_example, gitlab_example, self_hosted_example

[autofetch:github_example]
root = gh_simple
zip_root = simple-master
check_url = https://api.github.com/repos/fholmer/simple/git/refs/heads/master
payload_url = https://github.com/fholmer/simple/archive/refs/heads/master.zip

[autofetch:gitlab_example]
root = gl_simple
zip_root = simple-master
check_url = https://gitlab.com/api/v4/projects/fholmer%%2Fsimple/repository/branches/master
payload_url = https://gitlab.com/fholmer/simple/-/archive/master/simple-master.zip
headers = User-agent: Mozilla/5.0

[autofetch:self_hosted_example]
root = simple
zip_root = simple
check_url = https://example.local/api/v1/state/simple
payload_url = https://example.local/api/v1/download/zip/simple
headers = Token: NO, Host: distribute
"""


class GetEnvInterpolation(configparser.ExtendedInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        if value.startswith("${hook:env:"):
            env = value[11:-1]
            env_val = hooks.getenv(env)
            if env_val is None:
                raise ValueError(f"environment variable {env} not found.")
            return env_val
        elif value.startswith("${hook:keyring:"):
            keyring_opt = value[15:-1]
            keyring_val = hooks.getkeyring(keyring_opt)
            if keyring_val is None:
                raise ValueError(f"Keyring service {keyring_opt} not found.")
            return keyring_val
        return super().before_get(parser, section, option, value, defaults)


class Config:
    """
    Read config file or create one if it does not exist.
    """

    def __init__(self, config_file_path: str, host: str, port: int):
        self.config = configparser.ConfigParser(
            interpolation=GetEnvInterpolation(), delimiters=["="]
        )
        config_file = pathlib.Path.cwd().joinpath(config_file_path)
        if not config_file.exists():
            for config_string in self.init_config_file(config_file, []):
                self.config.read_string(config_string)
        else:
            self.config.read_string(default_config)
            self.config.read_string(config_file.read_text())
        self.config.read_dict({"autofetch": {"config": config_file_path}})
        # if host or port is set from command line arguments these
        # should be used instead of the configured host/port
        if host:
            self.config.set("server", "host", host)
        if port:
            self.config.set("server", "port", str(port))

        self.parse_hooks()

    @classmethod
    def init_config_file(
        cls, config_file: pathlib.Path, extra_config_string_list: "list[str]"
    ) -> str:
        config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=["/"],
            delimiters=["="],
        )
        # auto generate token
        config_string_list = [
            default_config,
            f"""
            [server]
            write_token = {cls.generate_token()}
            read_token = {cls.generate_token()}
            """,
        ]
        config_string_list.extend(extra_config_string_list)
        # ensure that folders exists
        config_file.parent.mkdir(parents=True, exist_ok=True)
        for config_string in config_string_list:
            config.read_string(config_string)
        with config_file.open(mode="w") as f:
            config.write(f)
        return config_string_list

    def parse_hooks(self):
        for section_name, section in self.config.items():
            if section_name.startswith("hook:"):
                pass  # TODO: implement hook sections
            else:
                for option_name, option in section.items():
                    if option_name.startswith("hook:"):
                        hooks.register.hook_entrypoint(
                            section_name, option_name, option
                        )

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)


def parse(config_file: str, host: str, port: int) -> configparser.ConfigParser:
    """
    Return a object that holds config info
    """
    config = Config(config_file, host, port)
    return config.config


def config_init(config_file: str, cwd: str, merge: bool):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config_path = pathlib.Path(config_file).expanduser()

    if config_path.exists():
        if merge:
            Config.init_config_file(config_path, [config_path.read_text()])
            print(f"Merged {config_file} with default options")
        else:
            raise exceptions.CommandFail(f"Config file: {config_file} already exists.")
    else:
        Config(str(config_path), None, None)
        print(f"Created {config_file} with default options")


def config_set(section, option, value, config_file, cwd):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if config_path.exists():
        config.read_string(config_path.read_text())

    if not config.has_section(section):
        config.add_section(section)

    if config.has_option(section, option):
        old_value = config.get(section, option)
        if old_value == value:
            return

    config.set(section, option, value)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as f:
        config.write(f)


def config_get(section, option, config_file, cwd, all):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        interpolation=GetEnvInterpolation(),
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if not config_path.exists():
        raise exceptions.CommandFail("File not found")

    if all:
        config.read_string(default_config)
    config.read_string(config_path.read_text())

    res = config.get(section, option, fallback="")
    if res:
        print(res)
    else:
        raise exceptions.CommandFail("option not found")


def config_list(config_file, cwd, all):

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    config = configparser.ConfigParser(
        interpolation=GetEnvInterpolation(),
        allow_no_value=True,
        comment_prefixes=["/"],
        delimiters=["="],
    )
    config.optionxform = lambda option: option
    config_path = pathlib.Path(config_file).expanduser()

    if not config_path.exists():
        raise exceptions.CommandFail("File not found")

    if all:
        config.read_string(default_config)
    config.read_string(config_path.read_text())

    for section_name, section in config.items():
        print(f"[{section_name}]")
        for option_name, option in section.items():
            print(f"{option_name} = {option}")
        print("")


def generate_token():
    print(Config.generate_token())

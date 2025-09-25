import argparse
import os
import subprocess


def get_init_script_path_for_blender():
    return os.path.join(os.path.dirname(__file__), "blender", "__init__.py")


def get_etc_dir():
    return os.path.join(os.path.dirname(__file__), "etc")


def parse_args(args=None) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--blender", default="/usr/local/bin/blender")
    return parser.parse_known_args(args)


def main_short() -> None:
    args, remaining = parse_args()
    short_settings_path = os.path.join(get_etc_dir(), "settings_for_short.json")
    for_short_args = ["-c", short_settings_path]
    cli_args = (
        [args.blender, "-P", get_init_script_path_for_blender(), "--"]
        + for_short_args
        + remaining
    )
    # print("slide2video_short: ", cli_args)
    subprocess.run(cli_args)


def main() -> None:
    args, remaining = parse_args()
    cli_args = [
        args.blender,
        "-P",
        get_init_script_path_for_blender(),
        "--",
    ] + remaining
    # print("slide2video: ", cli_args)
    subprocess.run(cli_args)

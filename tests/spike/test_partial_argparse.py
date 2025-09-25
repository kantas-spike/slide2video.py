import argparse

import slide2video
import slide2video.blender


def test_partial_parsing():
    """endpointではblenderオプションのみ解析し、残りはblenderの引数として渡す"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--blender", default="/usr/local/bin/blender")
    input_args1 = [
        "--blender",
        "/opt/bin/blender",
        "--config",
        "aaa",
        "--rate",
        "'aa 12'",
    ]
    args, remaining = parser.parse_known_args(input_args1)
    print(args, remaining)
    assert "/opt/bin/blender" == args.blender
    assert "--config aaa --rate 'aa 12'" == " ".join(remaining)

    input_args2 = ["--blender", "/opt/bin/blender"]
    args, remaining = parser.parse_known_args(input_args2)
    print(args, remaining)
    assert "/opt/bin/blender" == args.blender
    assert "" == " ".join(remaining)

    input_args3 = ["--blender", "/opt/bin/blender", "--help"]
    args, remaining = parser.parse_known_args(input_args3)
    print(args, remaining)
    assert "/opt/bin/blender" == args.blender
    assert "--help" == " ".join(remaining)


def test_module_path():
    print(slide2video.__file__)
    print(slide2video.blender.__file__)


def test_argparse_dup_options():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--blender", default="/usr/local/bin/blender")
    input_args1 = [
        "--blender",
        "/opt/bin/blender",
        "--blender",
        "/bin/blender",
        "--rate",
        "'aa 12'",
    ]
    args, remaining = parser.parse_known_args(input_args1)
    print(args, remaining)

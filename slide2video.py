import os
import sys
import json
import subprocess


def get_config():
    path = os.path.join(os.path.dirname(__file__), "settings.json")
    print(path)
    with open(path) as f:
        return json.load(f)


def usage():
    name = os.path.basename(__file__)
    print(f"USAGE: {name} SLIDE_DATA_DIR_PATH AUDIO_DATA_DIR_PATH")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("引数に、スライドデータと音声データのディレクトリを指定してください\n")
        usage()
        sys.exit(1)

    config = get_config()
    script_path = os.path.join(os.path.dirname(__file__), "slide2video_with_blender.py")
    cmd_line = [config["blender"], "-P", script_path, "--", sys.argv[1], sys.argv[2]]
    print(cmd_line)
    subprocess.run(cmd_line)

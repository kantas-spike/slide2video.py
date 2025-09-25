import argparse
import glob
import json
import os
import re
import sys

import bpy

DEFAULT_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "etc", "settings.json")
)
DEFAULT_BLENDER_PATH = "/usr/local/bin/blender"


def get_config(path):
    print(path)
    with open(path) as f:
        return json.load(f)


def get_no_from_path(path):
    if result := re.match(r"[^\d]*(\d+)[^\d]*", os.path.basename(path)):
        no = result.group(1)
        return int(no)
    else:
        raise Exception(f"Detected filename without numbers: {path}")


def get_data(slide_dir, audio_dir, config):
    slide_pattern = os.path.join(slide_dir, "*.{}".format(config.get("image", "jpg")))
    audio_pattern = os.path.join(audio_dir, "*.{}".format(config.get("audio", "wav")))
    slide_dic = {}
    audio_dic = {}

    for f in sorted(glob.glob(slide_pattern), key=lambda x: get_no_from_path(x)):
        no = get_no_from_path(f)
        slide_dic[no] = f

    for f in sorted(glob.glob(audio_pattern)):
        no = get_no_from_path(f)
        audio_dic[no] = f

    # print(slide_dic, audio_dic)

    data = {}
    for no in slide_dic.keys():
        slide_path = slide_dic[no]
        audio_path = audio_dic.get(no, None)
        data[no] = {"slide": slide_path, "audio": audio_path}

    return data


def get_framerate_preset(frame_rate):
    return bpy.utils.preset_find(str(frame_rate), "framerate")


def setup_render_settings(config):
    render = bpy.data.scenes["Scene"].render

    # 画面解像度
    render.resolution_x = config["resolution_x"]
    render.resolution_y = config["resolution_y"]
    render.resolution_percentage = config["resolution_percentage"]

    # Frame Rate
    preset_path = get_framerate_preset(config["frame_rate"])
    bpy.ops.script.execute_preset(
        filepath=preset_path,
        menu_idname="RENDER_MT_framerate_presets",
    )

    # File Format を FFMPEG に
    render.image_settings.file_format = "FFMPEG"

    # Encoding Container を MPEG-4 に
    render.ffmpeg.format = "MPEG4"

    # 動画出力先を指定(注:{blend_name}は.blendファイルの名前)
    render.filepath = "//{blend_name}.mp4"


def get_margin_x_frame(config):
    fps = config["render"]["frame_rate"]
    ml = config["audio"]["margin_left_sec"]
    mr = config["audio"]["margin_right_sec"]
    return (int(ml * fps), int(mr * fps))


def update_config(args):
    config = get_config(args.config)
    print("org config:", config)
    print("args:", args)
    if config["render"]["frame_rate"] != args.fps:
        config["render"]["frame_rate"] = args.fps
    if config["render"]["resolution_percentage"] != args.percentage:
        config["render"]["resolution_percentage"] = args.percentage
    print("new config:", config)
    return config


def view_all():
    for w in bpy.context.window_manager.windows:
        for a in w.screen.areas:
            if a.type == "SEQUENCE_EDITOR" and a.spaces[0].view_type == "SEQUENCER":
                for r in a.regions:
                    if r.type == "WINDOW":
                        print(a.type)
                        print(r.type)
                        with bpy.context.temp_override(window=w, area=a, region=r):
                            # bpy.ops.sequencer.view_all() を直接呼ぶと表示が崩れるため以下で対応
                            bpy.ops.sequencer.view_selected()
                            bpy.ops.sequencer.select_all(action="DESELECT")
                            return


def parse_args(script_args):
    render_config = get_config(DEFAULT_CONFIG_PATH)["render"]

    parser = argparse.ArgumentParser(
        prog="slide2video",
        description="指定されたスライドデータとオーディオデータからBlenderプロジェクトを作成する",
    )
    parser.add_argument(
        "slide_data",
        metavar="SLIDE_DIR",
        type=str,
        help="スライドデータを格納したディレクトリのパス",
    )
    parser.add_argument(
        "audio_data",
        metavar="AUDIO_DIR",
        type=str,
        help="音声データを格納したディレクトリのパス",
    )
    parser.add_argument(
        "blend_file",
        metavar="BLEND_FILE",
        type=str,
        help="作成するBlenderプロジェクトファイルのパス",
    )
    parser.add_argument(
        "--blender",
        default=DEFAULT_BLENDER_PATH,
        metavar="BLENDER_PATH",
        help=f"blenderコマンドのパス: デフォルト値: {DEFAULT_BLENDER_PATH}",
    )

    parser.add_argument(
        "-r",
        "--fps",
        metavar="FRAME_RATE",
        type=int,
        default=render_config["frame_rate"],
        help=f"フレームレート(fps). デフォルト値: {render_config['frame_rate']}",
    )
    parser.add_argument(
        "-p",
        "--percentage",
        metavar="RESOLUTION_PERCENTAGE",
        type=int,
        default=render_config["resolution_percentage"],
        help=f"解像度のパーセンテージ. デフォルト値: {render_config['resolution_percentage']}",
    )
    parser.add_argument(
        "-c",
        "--config",
        metavar="CONFIG_PATH",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help=f"設定ファイルのパス. デフォルト値: {DEFAULT_CONFIG_PATH}",
    )

    args = parser.parse_args(script_args)

    return args


def setup_strips(data, config):
    se = bpy.context.scene.sequence_editor
    f_start = 1
    audio_channel = 2
    image_channel = 3

    default_num_of_frames = config["image"]["default_num_of_frames"]

    ml_frame, mr_frame = get_margin_x_frame(config)
    print(ml_frame, mr_frame)

    for item in data.values():
        image, audio = item["slide"], item["audio"]
        # Use special relative paths starting with '//' in Blender,
        # it meaning relative from the Blender file.
        image = bpy.path.relpath(image)
        if audio:
            audio = bpy.path.relpath(audio)
        print(audio, image)

        if audio is not None:
            snd = se.sequences.new_sound(
                os.path.basename(audio), audio, audio_channel, (f_start + ml_frame)
            )
            snd.show_waveform = True
            frame_end = snd.frame_final_end + mr_frame
        else:
            frame_end = f_start + default_num_of_frames + ml_frame + mr_frame

        img = se.sequences.new_image(
            os.path.basename(image), image, image_channel, f_start, fit_method="FIT"
        )
        img.frame_final_end = frame_end
        f_start = frame_end

    bpy.data.scenes["Scene"].frame_end = f_start

    # 全てのストリップをビューに表示
    view_all()


def create_blend_file(blend_file_path):
    blend_file_dir = os.path.dirname(blend_file_path)

    # New File VideoEditing
    bpy.context.preferences.view.show_splash = False
    bpy.ops.wm.read_homefile(app_template="Video_Editing")

    if not os.path.exists(blend_file_dir):
        os.makedirs(blend_file_dir)

    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)


def main():
    # -- 以降の引数を取得
    script_args = sys.argv[sys.argv.index("--") + 1 :]
    # print(script_args)

    # 引数を解析
    args = parse_args(script_args)

    # 引数の値をもとに設定を更新
    config = update_config(args)

    # スライドの画像と音声データを取得
    data = get_data(args.slide_data, args.audio_data, config["extension"])
    # print(data)

    # save blend file
    blend_file_path = os.path.abspath(os.path.expanduser(args.blend_file))

    # .blendファイルを作成('//'パスでリソース保存するために事前にblendファイルを作成)
    create_blend_file(blend_file_path)

    # render設定を更新
    setup_render_settings(config["render"])

    # 画像、音声stripを配置
    setup_strips(data, config)

    # .blendファイルを保存
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)


if __name__ == "__main__":
    main()

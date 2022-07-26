import bpy
import os
import re
import sys
import glob
from importlib import machinery


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


def setup_render(config, blend_file_dir):
    render = bpy.data.scenes["Scene"].render

    # 画面解像度
    render.resolution_x = config["resolution_x"]
    render.resolution_y = config["resolution_y"]
    render.resolution_percentage = config["resolution_percentage"]

    # Frame Rate
    bpy.ops.script.execute_preset(
        filepath="/Applications/Blender.app/Contents/Resources/3.2/scripts/presets/framerate/{}.py".format(
            config["frame_rate"]
        ),
        menu_idname="RENDER_MT_framerate_presets",
    )

    # File Format を FFMPEG に
    render.image_settings.file_format = "FFMPEG"

    # Encoding Container を MPEG-4 に
    render.ffmpeg.format = "MPEG4"

    # 動画出力ディレクトリを指定
    render.filepath = blend_file_dir + "/"


def load_slide2video_module():
    loader = machinery.SourceFileLoader(
        "slide2video", os.path.join(os.path.dirname(__file__), "slide2video.py")
    )
    return loader.load_module()


def get_margin_x_frame(config):
    fps = config["render"]["frame_rate"]
    ml = config["audio"]["margin_left_sec"]
    mr = config["audio"]["margin_right_sec"]
    return (int(ml * fps), int(mr * fps))


if __name__ == "__main__":
    common = load_slide2video_module()
    if len(sys.argv) < 4:
        print("引数に、スライドデータと音声データのディレクトリを指定してください\n")
        common.usage()
        sys.exit(1)

    config = common.get_config()

    data = get_data(sys.argv[-3], sys.argv[-2], config["extension"])
    # print(data)

    # New File VideoEditing
    bpy.context.preferences.view.show_splash = False
    bpy.ops.wm.read_homefile(app_template="Video_Editing")

    # save blend file
    #   blender独自の相対パスでリソース保存する場合は事前にblendファイル保存が必要なため
    blend_file_path = os.path.abspath(os.path.expanduser(sys.argv[-1]))
    blend_file_dir = os.path.dirname(blend_file_path)

    if not os.path.exists(blend_file_dir):
        os.makedirs(blend_file_dir)

    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)

    # renderを設定
    setup_render(config["render"], blend_file_dir)

    se = bpy.context.scene.sequence_editor
    f_start = 1
    audio_channel = 1
    image_channel = 3

    default_num_of_frames = config["image"]["default_num_of_frames"]

    ml_frame, mr_frame = get_margin_x_frame(config)
    print(ml_frame, mr_frame)

    for item in data.values():
        image, audio = item["slide"], item["audio"]
        # Use special relative paths starting with '//' in Blender, it meaning relative from the Blender file.
        image = bpy.path.relpath(image, start=blend_file_dir)
        audio = bpy.path.relpath(audio, start=blend_file_dir)
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

    # save blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)

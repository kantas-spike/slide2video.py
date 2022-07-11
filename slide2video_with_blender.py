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


def setup_render(config):
    render = bpy.data.scenes["Scene"].render

    # 画面解像度
    bpy.data.scenes["Scene"].render.resolution_x = config["resolution_x"]
    bpy.data.scenes["Scene"].render.resolution_y = config["resolution_y"]
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


def load_slide2video_module():
    loader = machinery.SourceFileLoader(
        "slide2video", os.path.join(os.path.dirname(__file__), "slide2video.py")
    )
    return loader.load_module()


if __name__ == "__main__":
    common = load_slide2video_module()
    if len(sys.argv) < 3:
        print("引数に、スライドデータと音声データのディレクトリを指定してください\n")
        common.usage()
        sys.exit(1)

    config = common.get_config()

    data = get_data(sys.argv[-2], sys.argv[-1], config["extension"])
    # print(data)

    bpy.context.preferences.view.show_splash = False

    # New File VideoEditing
    bpy.ops.wm.read_homefile(app_template="Video_Editing")

    # renderを設定
    setup_render(config["render"])

    se = bpy.context.scene.sequence_editor
    f_start = 1
    audio_channel = 1
    image_channel = 3

    default_num_of_frames = config["image"]["default_num_of_frames"]

    for item in data.values():
        image, audio = item["slide"], item["audio"]
        print(audio, image)

        if audio is not None:
            snd = se.sequences.new_sound(
                os.path.basename(audio), audio, audio_channel, f_start
            )
            snd.show_waveform = True
            frame_end = snd.frame_final_end
        else:
            frame_end = f_start + default_num_of_frames

        img = se.sequences.new_image(
            os.path.basename(image), image, image_channel, f_start, fit_method="FIT"
        )
        img.frame_final_end = frame_end
        f_start = frame_end

    bpy.data.scenes["Scene"].frame_end = f_start

# slide2video.py

本ツールは、スライド資料と、その資料用の音声データからBlenderの動画編集ファイルを作成するツールです。
実行すると、ビデオシーケンサーにスライドと音声が配置されたファイルが作成されます。

## 前提

スライド資料、および音声データファイルは以下のものを前提としています。

- `スライド資料`: "slide`1`.jpg"などの`スライド番号`をファイル名に含む画像ファイル。
- `音声データ`: "`1`_xxx.wav"などの`スライド番号`をファイル名に持つ音声ファイル。

各ファイル名の`スライド番号`から`スライド資料`と`音声データ`を対応付けます。

また、スライド資料は、[odp2jpg.sh](https://github.com/kantas-spike/odp2jpg.sh)を、音声データは、[vv_wav2slide_wav.py](https://github.com/kantas-spike/vv_wav2slide_wav.py)を使用して作成することもできます。

## 使い方

以下を実行します。

`SLIDE_DATA_DIR`と`AUDIO_DATA_DIR`は、それぞれ、`スライド資料`と`音声データ`を格納したディレクトリのパスです。

~~~sh
python3 slide2video.py SLIDE_DATA_DIR AUDIO_DATA_DIR
~~~

実行の結果、Blenderの`Video Editing`を起動し、
スライド資料と音声データを対応づけて、ビデオシーケンサーのチャンネルに配置します。

この時点で、ビデオシーケンサーを再生すれば、スライド＋音声のプレビューを確認できます。必要があれば、効果や字幕を手動で追加してください。

## カスタマイズ

本ツールは、設定ファイル(`settings.json`)によりカスタマイズできます。
必要に応じて変更してください。

### `settings.json`の例

~~~json
{
    "render": {
        "resolution_x": 1920,
        "resolution_y": 1080,
        "resolution_percentage": 50,
        "frame_rate": 30
    },
    "image": {
        "default_num_of_frames": 30
    },
    "extension": {
        "image": "jpg",
        "audio": "wav"
    },
    "blender": "/Applications/Blender.app/Contents/MacOS/Blender"
}
~~~

### `settings.json`の設定項目の説明

|キー|サブキー|説明|デフォルト値|
|:--:|:---:|:---|:---|
|render|resolution_x|レンダリング結果の水平解像度|1920|
|render|resolution_y|レンダリング結果の垂直解像度|1080|
|render|resolution_percentage|レンダリング解像度の割合(単位:%)|50|
|render|frame_rate|レンダリング結果のフレームレート(単位:fps)|30|
|image|default_num_of_frames|スライドに対応する音声ファイルがない場合のスライドの表示フレーム数|30|
|extension|image|スライド画像ファイルの拡張子|jpg|
|extension|audio|音声データファイルの拡張子|wav|
|blender|-|コマンドライン起動時に使用するBlenderコマンドのパス|/Applications/Blender.app/Contents/MacOS/Blender|


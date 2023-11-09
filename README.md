# slide2video.py

本ツールは、スライド資料と、その資料用の音声データからBlenderの動画編集ファイルを作成するツールです。
実行すると、ビデオシーケンサーにスライドと音声が配置されたファイルが作成されます。

## 前提

スライド資料、および音声データファイルは以下のものを前提としています。

- `スライド資料`: "slide`1`.jpg"などの`スライド番号`をファイル名に含む画像ファイル。
- `音声データ`: "`1`\_xxx.wav"などの`スライド番号`をファイル名に持つ音声ファイル。

各ファイル名の`スライド番号`から`スライド資料`と`音声データ`を対応付けます。

また、スライド資料は、[odp2jpg.sh](https://github.com/kantas-spike/odp2jpg.sh)を、音声データは、[vv_wav2slide_wav.py](https://github.com/kantas-spike/vv_wav2slide_wav.py)を使用して作成することもできます。

## 使い方

以下を実行します。(`SLIDE_DATA_DIR`と`AUDIO_DATA_DIR`は、それぞれ、`スライド資料`と`音声データ`を格納したディレクトリのパスです。)

```shell
~/bin/slide2video.sh SLIDE_DATA_DIR AUDIO_DATA_DIR BLEND_FILE_PATH
```

実行の結果、Blenderの`Video Editing`を起動し、
スライド資料と音声データを対応づけて、ビデオシーケンサーのチャンネルに配置します。

この時点で、ビデオシーケンサーを再生すれば、スライド＋音声のプレビューを確認できます。必要があれば、効果や字幕を手動で追加してください。

### ヘルプ

```shell
~/bin/slide2video.sh -h
usage: slide2video.sh [-h] [-r FRAME_RATE] [-p RESOLUTION_PERCENTAGE] SLIDE_DIR AUDIO_DIR BLEND_FILE

指定されたスライドデータとオーディオデータからBlenderプロジェクトを作成する

positional arguments:
  SLIDE_DIR             スライドデータを格納したディレクトリのパス
  AUDIO_DIR             音声データを格納したディレクトリのパス
  BLEND_FILE            作成するBlenderプロジェクトファイルのパス

options:
  -h, --help            show this help message and exit
  -r FRAME_RATE, --fps FRAME_RATE
                        フレームレート(fps). デフォルト値: 60
  -p RESOLUTION_PERCENTAGE, --percentage RESOLUTION_PERCENTAGE
                        解像度のパーセンテージ. デフォルト値: 100
```

## インストール方法

`Makefile`にインストール先ディレクトリと、`Blender`コマンドのパスが変数に定義されています。 環境に合せて以下の変数を修正し、

```shell
# 環境に合せてインストール先とBlenderコマンドを変更してください
DST_BIN=${HOME}/bin
DST_DIR=${HOME}/opt/slide2video
BLENDER_COMMAND=/Applications/Blender.app/Contents/MacOS/Blender
```

以下のコマンドでインストールできます。

デフォルトでは、`~/bin`に`slide2video.sh`がインストールされます。 なお、`bin/slide2video.sh`は、`~/opt/bin/slide2vidoe.sh`のシンボリックリンクになります。

```shell
make install
```

また、以下でインストールしたスクリプトを削除できます。

```shell
make clean
```

## カスタマイズ

本ツールは、設定ファイル(`settings.json`)によりカスタマイズできます。
必要に応じて変更してください。

### `settings.json`の例

```json
{
  "render": {
    "resolution_x": 1920,
    "resolution_y": 1080,
    "resolution_percentage": 100,
    "frame_rate": 60
  },
  "image": {
    "default_num_of_frames": 30
  },
  "audio": {
    "margin_left_sec": 0.8,
    "margin_right_sec": 1.0
  },
  "extension": {
    "image": "jpg",
    "audio": "wav"
  }
}
```

### `settings.json`の設定項目の説明

|   キー    |       サブキー        | 説明                                                               | デフォルト値 |
| :-------: | :-------------------: | :----------------------------------------------------------------- | :----------- |
|  render   |     resolution_x      | レンダリング結果の水平解像度                                       | 1920         |
|  render   |     resolution_y      | レンダリング結果の垂直解像度                                       | 1080         |
|  render   | resolution_percentage | レンダリング解像度の割合(単位:%)                                   | 100          |
|  render   |      frame_rate       | レンダリング結果のフレームレート(単位:fps)                         | 60           |
|   image   | default_num_of_frames | スライドに対応する音声ファイルがない場合のスライドの表示フレーム数 | 30           |
|   audio   |    margin_left_sec    | スライド表示してから音声ファイル再生までの待ち時間(単位:秒)        | 0.8          |
|   audio   |   margin_right_sec    | 音声ファイル再生終了から次のスライド表示までの待ち時間(単位:秒)    | 1.0          |
| extension |         image         | スライド画像ファイルの拡張子                                       | jpg          |
| extension |         audio         | 音声データファイルの拡張子                                         | wav          |

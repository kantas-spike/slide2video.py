# リリース用(1) or 開発用(0)
RELEASE ?= 1

# 環境に合せてインストール先とBlenderコマンドを変更してください
ifeq ($(RELEASE), 1)  # リリース用設定
	DST_BIN=${HOME}/bin
	DST_DIR=${HOME}/opt/slide2video
else  # 開発用設定
	DST_BIN=./bin
	DST_DIR=./build/slide2video
endif
BLENDER_COMMAND=/Applications/Blender.app/Contents/MacOS/Blender


WK_DIR=./build

TARGET_SHELL=$(WK_DIR)/slide2video.sh
TARGET_SHORT_SHELL=$(WK_DIR)/slide2video_short.sh

$(TARGET_SHELL): ./build/slide2video.sh.tmpl
	cat $< | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${DST_DIR}#' | sed -e 's#@@@BLENDER_COMMAND@@@#${BLENDER_COMMAND}#' > $@

$(TARGET_SHORT_SHELL): ./build/slide2video_short.sh.tmpl
	cat $< | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${DST_DIR}#' | sed -e 's#@@@BLENDER_COMMAND@@@#${BLENDER_COMMAND}#' > $@

clean:
	rm $(TARGET_SHELL)
	rm $(TARGET_SHORT_SHELL)
	rm ${DST_BIN}/slide2video.sh
	rm ${DST_BIN}/slide2video_short.sh
	rm -r ${DST_DIR}

install: $(TARGET_SHELL) $(TARGET_SHORT_SHELL)
	mkdir -p ${DST_DIR}/bin
	mkdir -p ${DST_DIR}/lib
	mkdir -p ${DST_DIR}/etc
	cp -p $^ ${DST_DIR}/bin
	cp -p lib/*.py ${DST_DIR}/lib/
	cp -p etc/settings*.json ${DST_DIR}/etc/
	for f in $(^F) ; \
	do \
		chmod u+x ${DST_DIR}/bin/$$f ; \
		ln -s $(abspath ${DST_DIR}/bin/$$f) ${DST_BIN}/$$f ; \
	done



reinstall:
	make clean
	make install

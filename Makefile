# 環境に合せてインストール先とBlenderコマンドを変更してください
DST_BIN=${HOME}/bin
DST_DIR=${HOME}/opt/slide2video
BLENDER_COMMAND=/Applications/Blender.app/Contents/MacOS/Blender


bin/slide2video.sh: build/slide2video.sh.tmpl
	cat $< | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${DST_DIR}#' | sed -e 's#@@@BLENDER_COMMAND@@@#${BLENDER_COMMAND}#' > $@

install: bin/slide2video.sh
	mkdir -p ${DST_BIN}
	mkdir -p ${DST_DIR}/bin
	mkdir -p ${DST_DIR}/lib
	mkdir -p ${DST_DIR}/etc
	cp -p $< ${DST_DIR}/bin
	cp -p src/*.py ${DST_DIR}/lib/
	cp -p etc/settings.json ${DST_DIR}/etc/
	chmod u+x ${DST_DIR}/bin/$(<F)
	ln -s ${DST_DIR}/bin/$(<F) ${DST_BIN}/$(<F)

clean:
	rm ${DST_BIN}/slide2video.sh
	rm -r ${DST_DIR}

reinstall:
	make clean
	make install

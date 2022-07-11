DST_DIR=${HOME}/bin
SCRIPT_HOME=$(dir $(abspath slide2video.py))


slide2video.sh: slide2video.sh.tmpl
	cat slide2video.sh.tmpl | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${SCRIPT_HOME}#' > $@

clean: slide2video.sh
	rm $^

install: slide2video.sh
	mkdir -p ${DST_DIR}
	cp $< ${DST_DIR}
	chmod u+x ${DST_DIR}/$<
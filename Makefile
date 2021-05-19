INSTALL_PATH = /usr/local/bin/bc2

.PHONY: install

install:
	python3 -m pip install -r requirements.txt
	chmod u+x main.py
	ln -s $(shell pwd)/main.py $(INSTALL_PATH)

uninstall:
	unlink $(INSTALL_PATH)
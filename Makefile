# ex: set ts=8 noet:

all: qt6 test

test: testpy3

testpy3:
	python3 -m unittest discover tests

qt6: qt6py3

qt6py3:
	# PyQt6 removed pyrcc6 — use rcc from the Qt6 SDK if resources.py needs regeneration:
	#   rcc -g python -o libs/resources.py resources.qrc
	@echo "Note: pyrcc6 is removed in PyQt6. Use Qt6 SDK 'rcc -g python' to regenerate libs/resources.py"

clean:
	rm -rf ~/.labelImgSettings.pkl *.pyc dist labelImg.egg-info __pycache__ build

pip_upload:
	python3 setup.py upload

long_description:
	restview --long-description

.PHONY: all

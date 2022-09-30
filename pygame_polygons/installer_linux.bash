#!/usr/bin/env bash

pyinstaller \
      --log-level=WARN \
      --onefile \
      --nowindow \
      --key 123456 \
      --upx-dir=D:\ups\upx-3.96-win64 \
      --icon=resources/icon.icoicon.ico \
      -name pygame_polygons \
      main.py


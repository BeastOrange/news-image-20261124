#!/bin/sh
set -eu

cd "$(dirname "$0")"

python3 build_image.py entry.png
python3 build_image.py /tmp/news-image-20261124-check.png
cmp entry.png /tmp/news-image-20261124-check.png
md5sum entry.png
ls -l entry.png

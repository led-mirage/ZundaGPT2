# build_tools/build.sh
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

rm -rf build dist
pyinstaller --onefile --noconsole \
  --paths=./app \
  --add-data "./app/html:html" \
  --add-data "assets/ZundaGPT2-Icon64.png:assets" \
  --name ZundaGPT2 \
  --splash assets/ZundaGPT2_splash.png \
  app/main.py

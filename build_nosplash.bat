pyivf-make_version --source-format yaml --metadata-source version.yaml --outfile version.txt
pyinstaller --onefile --noconsole --paths=./app --add-data "./app/html;html" --name ZundaGPT2.ns --icon assets/ZundaGPT2.ico --version-file=version.txt app/main.py

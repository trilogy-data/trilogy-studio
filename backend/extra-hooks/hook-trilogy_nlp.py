from PyInstaller.utils.hooks import get_package_paths

datas = [(get_package_paths("trilogy_nlp")[1], "trilogy_nlp")]

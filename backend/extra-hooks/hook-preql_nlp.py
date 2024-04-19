from PyInstaller.utils.hooks import get_package_paths

datas = [(get_package_paths("preql_nlp")[1], "preql_nlp")]

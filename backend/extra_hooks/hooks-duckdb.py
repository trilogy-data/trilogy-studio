from PyInstaller.utils.hooks import get_package_paths

datas = [(get_package_paths("duckdb")[1], "duckdb")]

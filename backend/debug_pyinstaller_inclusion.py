import trilogy_public_models
from pathlib import Path
import sys

def get_trilogy_data_files():
    root = sys.modules.get('trilogy_public_models')
    root = Path(root.__file__)

    inclusion_files = []
    for key, value in trilogy_public_models.models.items():
    
        path = key.replace('.' , '/')

        check = root.parent / path

        files = check.iterdir()
        for f in files:
            if f.suffix == '.preql':
                subroot = Path('trilogy_public_models') / path
                inclusion_files.append(( str(f), str(subroot)))
    return inclusion_files

if __name__ == "__main__":

    inclusion_files = get_trilogy_data_files()
    print('----')
    for f in inclusion_files:
        print(f)
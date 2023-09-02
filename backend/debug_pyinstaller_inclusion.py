import trilogy_public_models
import pkgutil
from pathlib import Path
import sys
root = sys.modules.get(f'trilogy_public_models')

print(root.__file__)

root = Path(root.__file__)

for key, value in trilogy_public_models.models.items():
   
    path = key.replace('.' , '/')

    check = root.parent / path

    files = check.iterdir()
    for f in files:
        print(f)
from pathlib import Path

from trilogy_public_models.inventory import parse_initial_models
from trilogy_public_models import models


def get_trilogy_data_files():
    search_path = '/home/edickinson/preql-studio/backend/dist/trilogy-studio-engine-debug/trilogy_public_models'

    test = Path(search_path)

    for item in test.glob('**/*preql'):
        # prnt(item)
        
        if item.name == 'entrypoint.preql':
            relative = item.parent.relative_to(test)
            model = parse_initial_models(str(item))
            models[str(relative).replace('/', '.')] = model
    return []
    # inclusion_files = []
    # for key, value in trilogy_public_models.models.items():
    
    #     path = key.replace('.' , '/')

    #     check = root.parent / path

    #     files = check.iterdir()
    #     for f in files:
    #         if f.suffix == '.preql':
    #             subroot = Path('trilogy_public_models') / path
    #             inclusion_files.append(( str(f), str(subroot)))
    # return inclusion_files

if __name__ == "__main__":

    inclusion_files = get_trilogy_data_files()
    for key, val in models.items():
        print(key)
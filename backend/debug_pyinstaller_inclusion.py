import trilogy_public_models
import pkgutil


for key, value in trilogy_public_models.models.items():
    print(key)
    path = key.replace('.' , '/')
    trilogy_public_model_data = pkgutil.get_data('trilogy_public_models', f'{path}' )

    print(trilogy_public_model_data)
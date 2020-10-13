import os
from . import settings


def setting_from_object(obj):
    setting = dict()
    for key in dir(obj):
        setting[key] = getattr(obj, key)
    return setting


settings = setting_from_object(settings)

settings.update({
        'UPLOAD_PATH':os.path.join(os.path.dirname(__file__), 'upload'),
    })

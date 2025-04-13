import os.path


def user_directory_path(instance, filename):
    storage_title = instance.storage_title
    return os.path.join(instance.owner.username, str(storage_title))

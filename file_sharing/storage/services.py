import os.path


def user_directory_path(instance, filename):
    print('instance =', instance, filename)
    # return os.path.join(instance.owner.username, filename)
    # return '%s/%s' % (instance.owner.username, filename)
    storage_title = instance.storage_title
    return os.path.join(instance.owner.username, str(storage_title))

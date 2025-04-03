import os.path


def user_directory_path(instance, filename):
    print('instance =', instance)
    # return os.path.join(instance.owner.username, filename)
    return '%s/%s' % (instance.owner.username, filename)

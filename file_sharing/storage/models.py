import uuid

from django.db import models
from django.conf import settings as st

from storage.services import user_directory_path


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    original_title = models.CharField(max_length=100, blank=True)
    comment = models.TextField(blank=True)
    storage_title = models.UUIDField(default=uuid.uuid4)
    size = models.BigIntegerField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    last_download = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    owner = models.ForeignKey(st.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files', blank=True)
    # path = models.FilePathField(path=os.path.join(owner.folder_path, storage_title))
    link = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.original_title

    def save(self, *args, **kwargs):
        # print(self.file.name, self.storage_title)
        if str(self.storage_title) not in self.file.name:
            # print(self)
            # self.original_title = self.request.original_title
            self.size = self.file.size
            self.file.name = str(self.storage_title)
            self.link = self.file.path
            super().save(*args, **kwargs)
            # self.link = self.file.path
            self.file.name = str(self.storage_title)
        else:
            # print('else')
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(File, self).delete(*args, **kwargs)
        storage.delete(path)

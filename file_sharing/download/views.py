from django.http import FileResponse

from storage.models import File


def file_download(request, storage_title):
    file = File.objects.get(storage_title=storage_title)
    link = file.file
    title = file.original_title
    return FileResponse(link, as_attachment=True, filename=title)

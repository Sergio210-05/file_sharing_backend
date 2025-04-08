import datetime

from django.http import FileResponse

from storage.models import File


def file_download(request, storage_title):
    file = File.objects.get(storage_title=storage_title)
    link = file.file
    title = file.original_title
    file.last_download = datetime.datetime.now()
    file.save(update_fields=['last_download'])
    response = FileResponse(link, as_attachment=True, filename=title)
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    # response["Content-Disposition"] = 'attachment; filename="your_file_name"'
    return response

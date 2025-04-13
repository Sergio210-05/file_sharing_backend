import datetime
import uuid

from django.http import FileResponse, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentification.models import User
from storage.models import File
from storage.permissions import IsAdminOrOwner
from storage.serializers import FileSerializer


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['owner', 'storage_title']
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def list(self, request, *args, **kwargs):
        user_id = int(self.request.GET.get('memberId', 0))
        if user_id > 0:
            user = User.objects.get(pk=user_id)
            query_set = File.objects.filter(owner=user).order_by('id')
            response = self.serializer_class(query_set, many=True).data
            # return Response(self.serializer_class(query_set, many=True).data,
        #                     status=status.HTTP_200_OK)
        # return Response([], status=status.HTTP_200_OK)
            return JsonResponse({'data': response}, status=status.HTTP_200_OK)
        return JsonResponse({'data': []}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        file = File.objects.get(pk=pk)
        file.last_download = datetime.datetime.now()
        file.save()
        link = file.file
        title = file.original_title
        return FileResponse(link, as_attachment=True, filename=title)

    def perform_create(self, serializer):
        user_id = self.request.data.get('member_id', self.request.user.id)
        user = User.objects.get(pk=int(user_id))
        serializer.save(owner=user,
                        original_title=self.request.data['original_title'],
                        storage_title=uuid.uuid4(),
                        )

    def update(self, request, pk=None, *args, **kwargs):
        instance = File.objects.get(pk=pk)
        if request.user.is_authenticated:
            instance.original_title = request.data.get("original_title", instance.original_title)
            instance.comment = request.data.get("comment", instance.comment)
            instance.save(update_fields=['original_title', 'comment'])
            return JsonResponse({'detail': 'Параметры файла обновлены'}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Вы неавторизованы'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'detail': f'Файл {instance.original_title} удалён'},
                            status=status.HTTP_204_NO_CONTENT)

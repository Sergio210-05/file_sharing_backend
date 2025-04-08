import datetime
import uuid

from django.http import FileResponse, JsonResponse
from django.shortcuts import render
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

    # def get_queryset(self):
    #     print('request path:', self.request.path)
    #     print('request memberId:', self.request.GET.get('memberId', None))
    #     user_id = int(self.request.GET.get('memberId', 0))
    #     if user_id > 0:
    #         user = User.objects.get(pk=user_id)
    #         return File.objects.filter(owner=user)

    # def filter_queryset(self, queryset):
    #     print('request path:', self.request.path)
    #     print('request memberId:', self.request.GET.get('memberId', None))
    #     user_id = int(self.request.GET.get('memberId', 0))
    #     if user_id > 0:
    #         user = User.objects.get(pk=user_id)
    #         return File.objects.filter(owner=user)

    def list(self, request, *args, **kwargs):
        print('request path:', request.path)
        print('request memberId:', self.request.GET.get('memberId', None))
        user_id = int(self.request.GET.get('memberId', 0))
        if user_id > 0:
            user = User.objects.get(pk=user_id)
            query_set = File.objects.filter(owner=user).order_by('id')
            return Response(self.serializer_class(query_set, many=True).data,
                            status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # print('retrieve')
        file = File.objects.get(pk=pk)
        file.last_download = datetime.datetime.now()
        file.save()
        link = file.file
        title = file.original_title
        return FileResponse(link, as_attachment=True, filename=title)

    def perform_create(self, serializer):
        print('perform_create')
        user_id = self.request.data.get('member_id', self.request.user.id)
        user = User.objects.get(pk=int(user_id))
        print('user=', user)
        print('user.id=', user.id)
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
        return Response(status=status.HTTP_201_CREATED)

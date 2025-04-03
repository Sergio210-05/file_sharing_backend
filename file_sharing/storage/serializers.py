from rest_framework import serializers

from storage.models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['owner', 'original_title', 'storage_title',
                            'size', 'last_download', 'link', ]

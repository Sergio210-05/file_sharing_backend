from django.conf import settings as st
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=1,
                                     default=serializers.CreateOnlyDefault('_'),
                                     verbose_name='login')

    class Meta:
        model = st.AUTH_USER_MODEL
        fields = ["username", "full_name", "email", 'is_staff', 'is_superuser', ]

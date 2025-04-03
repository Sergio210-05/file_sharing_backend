from rest_framework.routers import DefaultRouter

from storage.views import FileViewSet

router = DefaultRouter()
router.register('storage', FileViewSet)

urlpatterns = router.urls

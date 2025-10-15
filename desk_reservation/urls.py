from django.urls import include, path
from rest_framework.routers import DefaultRouter
from desk_reservation import views

router = DefaultRouter()
router.register(f'desk', views.DeskViewSet, basename='desk')
router.register(f'floor', views.FloorViewSet, basename='floor')
router.register(f'users', views.UserViewSet, basename='user')
# router.register(f'api-auth', include('rest_framework.urls'), basename='api-auth')

urlpatterns = [
    path('', include(router.urls)),
]
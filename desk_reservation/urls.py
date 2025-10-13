from django.urls import include, path
from rest_framework.routers import DefaultRouter
from desk_reservation import views

router = DefaultRouter()
router.register(f'desk', views.DeskViewSet, basename='desk')
router.register(f'floor', views.FloorViewSet, basename='floor')

urlpatterns = [
    path('', include(router.urls)),
]
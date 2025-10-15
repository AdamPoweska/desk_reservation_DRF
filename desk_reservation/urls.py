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
    path('api-auth/', include('rest_framework.urls')), # 'http://127.0.0.1:8000/api-auth/login/' or 'http://127.0.0.1:8000/api-auth/logout/'
]

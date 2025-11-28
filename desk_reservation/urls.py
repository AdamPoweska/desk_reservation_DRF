from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from desk_reservation import views

router = DefaultRouter()
router.register(f'desk', views.DeskViewSet, basename='desk')
router.register(f'floor', views.FloorViewSet, basename='floor')
router.register(f'floor_desk', views.FloorDeskNestedViewSet, basename='floor_desk')
router.register(f'workers', views.WorkerViewSet, basename='workers')
router.register(f'reservations', views.ReservationViewSet, basename='reservations')

#nested routers 1st level
# desk_nested_router = NestedDefaultRouter(router, r'desk', lookup='desk')
# desk_nested_router.register(r'floor_desk', views.DeskNestedViewSet, basename='floor_desk')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(desk_nested_router.urls)),
    path('api-auth/', include('rest_framework.urls')), # 'http://127.0.0.1:8000/api-auth/login/' or 'http://127.0.0.1:8000/api-auth/logout/'
]

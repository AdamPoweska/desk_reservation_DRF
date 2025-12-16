from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_nested.routers import NestedDefaultRouter
from desk_reservation import views

router = DefaultRouter()
router.register(f'desk', views.DeskViewSet, basename='desk')
router.register(f'floor', views.FloorViewSet, basename='floor')
router.register(f'floor_desk_one', views.FloorDeskNestedViewSetOne, basename='floor_desk_one')
router.register(f'floor_desk_two', views.FloorDeskNestedViewSetTwo, basename='floor_desk_two')
router.register(f'floor_desk_three', views.FloorDeskNestedViewSetThree, basename='floor_desk_three')
router.register(f'floor_desk_four', views.FloorDeskNestedViewSetFour, basename='floor_desk_four')
router.register(f'floor_desk_five', views.FloorDeskNestedViewSetFive, basename='floor_desk_five')
router.register(f'floor_desk_six', views.FloorDeskNestedViewSetSix, basename='floor_desk_six')
router.register(f'workers', views.WorkerViewSet, basename='workers')
router.register(f'reservations', views.ReservationViewSet, basename='reservations')

#nested routers 1st level
# desk_nested_router = NestedDefaultRouter(router, r'floor', lookup='floordesks')
# desk_nested_router.register(r'desks', views.FloorDeskNestedViewSet, basename='desks')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(desk_nested_router.urls)),
    path('api-auth/', include('rest_framework.urls')), # 'http://127.0.0.1:8000/api-auth/login/' or 'http://127.0.0.1:8000/api-auth/logout/'
]

from django.urls import path
from . import views


urlpatterns = [
    path('api/groups/manager/users',views.ManagerView.as_view() ,name='manager-users'),
    path('api/groups/manager/users/<int:pk>',views.SingleManagerView.as_view(), name='manager-users-detail'),
    path('api/groups/delivery-crew/users',views.DeliveryCrewView.as_view(), name='delivery-crew'),
    path('api/groups/delivery-crew/users/<int:pk>', views.SingleDeliveryCrewView.as_view(),name='delivery-crew-detail'),
]


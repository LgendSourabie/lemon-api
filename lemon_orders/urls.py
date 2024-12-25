from django.urls import path
from . import views


urlpatterns = [

    path('api/orders',views.OrderView.as_view() ,name='orders'),
    path('api/orders/<int:pk>',views.SingleOrderView.as_view(), name='orders-detail'),
    
]


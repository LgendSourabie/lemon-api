from django.urls import path
from . import views


urlpatterns = [
    path('api/menu-items',views.MenuItemView.as_view(), name='menu-items'),
    path('api/menu-items/<str:menu_item>', views.SingleMenuItemView.as_view(), name='menu-item-detail'),
]

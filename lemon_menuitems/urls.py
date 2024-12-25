from django.urls import path
from . import views


urlpatterns = [
    path('api/menu-items',views.MenuItemView.as_view(), name='menu-items'),
    path('api/menu-items/<str:menu_item>', views.SingleMenuItemView.as_view(), name='menu-items-detail'),
    path('api/cart/menu-items', views.CartView.as_view(),name='cart-menu-items'),
    path('api/categories', views.CategoryView.as_view() , name='categories'),
    path('api/categories/<int:pk>', views.SingleCategoryView.as_view() , name='categories-detail'),
]

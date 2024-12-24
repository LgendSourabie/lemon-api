from django.contrib import admin
from lemon_menuitems.models import Category, Cart, MenuItem
# Register your models here.


admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
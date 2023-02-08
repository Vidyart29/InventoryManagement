from django.contrib import admin
from .models import User, Admin, Product, ProductCategorie, orderHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Product)
admin.site.register(ProductCategorie)
admin.site.register(orderHistory)

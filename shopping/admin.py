from django.contrib import admin
from shopping.models import Product, ShoppingCart

# register models to the admin.
admin.site.register(Product)
admin.site.register(ShoppingCart)

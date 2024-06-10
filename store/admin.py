from django.contrib import admin
from .models import Cateogry, Customer, Product, Order

# Register your models here
admin.site.register(Cateogry)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

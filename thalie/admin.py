
# Register your models here.
from django.contrib import admin
from .models import (Product, Category,Brand, 
                     News, StockHistory, Store,Inventory)



admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(News)
admin.site.register(StockHistory)
admin.site.register(Store)
admin.site.register(Inventory)






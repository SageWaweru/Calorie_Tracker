from django.contrib import admin
from .models import FoodCategory, Food, Image, FoodLog, Weight

admin.site.register(FoodCategory)
admin.site.register(Food)
admin.site.register(Image)
admin.site.register(FoodLog)
admin.site.register(Weight)


# Register your models here.

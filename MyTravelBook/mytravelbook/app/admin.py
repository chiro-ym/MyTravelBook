from django.contrib import admin
from .models import TravelRecord, Prefecture, User, Category, Photo

# Register your models here.
admin.site.register(User)
admin.site.register(TravelRecord)
admin.site.register(Prefecture)
admin.site.register(Category)
admin.site.register(Photo)
from django.contrib import admin
from .models import TravelRecord, Prefecture, User

# Register your models here.
admin.site.register(User)
admin.site.register(TravelRecord)
admin.site.register(Prefecture)
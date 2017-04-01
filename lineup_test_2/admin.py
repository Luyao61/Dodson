from django.contrib import admin
from .models import Users, EyewitnessStimuli, Response

# Register your models here.
admin.site.register(EyewitnessStimuli)
admin.site.register(Users)
admin.site.register(Response)

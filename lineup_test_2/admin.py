from django.contrib import admin
from .models import User, EyewitnessStimuli, Response

# Register your models here.
admin.site.register(EyewitnessStimuli)
admin.site.register(User)
admin.site.register(Response)

from django.contrib import admin
from .models import Skillset, User

admin.site.site_header ="Online Job Recrutment System"

admin.site.register(User)
admin.site.register(Skillset)

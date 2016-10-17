from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hackathon)
admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(UserRoles)
admin.site.register(UserLanguage)


from django.contrib import admin
from .models import Certification, Education, Experience, Project

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Certification)

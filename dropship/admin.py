from django.contrib import admin

from .models import User, Project, Issue, Member

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Member)

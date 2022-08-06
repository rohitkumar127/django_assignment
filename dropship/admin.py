from django.contrib import admin

from .models import User, Project, Issue, Member, Sprint, Comment

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Member)
admin.site.register(Sprint)
admin.site.register(Comment)

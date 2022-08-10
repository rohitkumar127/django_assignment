from django.contrib import admin

from .models import User, Project, Issue,Label,Comment,Sprint,Worklog,IssueWatcher

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Label)
admin.site.register(Comment)
admin.site.register(Sprint)
admin.site.register(Worklog)
admin.site.register(IssueWatcher)

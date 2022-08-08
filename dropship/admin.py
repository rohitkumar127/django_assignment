from django.contrib import admin

from dropship import models

admin.site.register(models.User)
admin.site.register(models.Project)
admin.site.register(models.Issue)
admin.site.register(models.Member)
admin.site.register(models.Sprint)
admin.site.register(models.Comment)
admin.site.register(models.Label)

from django.contrib.auth.models import AbstractUser
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    # If there are any fields needed add here.
    role=models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.username


class Project(TimestampModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="creator",null=False)


    def __str__(self):
        return "{0} {1}".format(self.creator, self.title)

class Sprint(models.Model):
    project=models.ForeignKey(User,on_delete=models.CASCADE,related_name='project',null=False)
    start_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()
    sprint_status=models.BooleanField()

class Label:
    label=models.CharField(max_length=30,primary_key=True)

class Issue(TimestampModel):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    reporter=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='reporter',null=True)

    assignee=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='assignee')

    status=models.CharField(max_length=30)

    watchers=models.ManyToManyField(User,blank=True)

    sprint=models.ForeignKey(Sprint,blank=True,related_name='sprint',on_delete=models.CASCADE)

    label=models.ManyToManyField(Label,blank=True)

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=False
    )

    def __str__(self):
        return "{0}-{1}".format(self.project.creator, self.title)

class Comment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='user',null=False)
    issue=models.ForeignKey(Issue,on_delete=models.CASCADE,related_name='issue',null=False)
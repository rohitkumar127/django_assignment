from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    # If there are any fields needed add here.
    role = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Project(TimestampModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="creator", null=False)

    def __str__(self):
        return "{0} {1}".format(self.creator, self.title)


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', null=False)
    sprint_title = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    # start:0,stop:1 not started:null
    sprint_status = models.BooleanField(blank=True, null=True)


class Label(models.Model):
    label = models.CharField(max_length=30, primary_key=True)


class Issue(TimestampModel):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reporter_id', null=True)

    assignee = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='assignee')

    OPEN = 'open'
    INPRGRESS = 'in progress'
    INREVIEW = 'in review'
    CodeComplete = 'code complete '
    QATesting = 'qa testing'
    DONE = 'done'
    STATUS = [(OPEN, OPEN), (INPRGRESS, INPRGRESS), (INREVIEW, INREVIEW), (CodeComplete, CodeComplete),
              (QATesting, QATesting), (DONE, DONE)]

    status = models.CharField(max_length=30, choices=STATUS, default=OPEN, null=False)

    watchers = models.ManyToManyField(User, blank=True)

    sprint = models.ForeignKey(Sprint, blank=True, related_name='sprint', on_delete=models.CASCADE, null=True)

    label = models.ManyToManyField(Label, blank=True)

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=False
    )

    def __str__(self):
        return "{0}-{1}".format(self.project.creator, self.title)


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user', null=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue', null=False)

class Worklog(models.Model):
    time_spent=models.CharField(max_length=10)
    start_date=models.DateField()
    remaining_estimation=models.CharField(max_length=10)
    work_description=models.TextField()
    issue=models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_worklog', null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_worklog', null=False)

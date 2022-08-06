from pickle import TRUE
from django.contrib.auth.models import AbstractUser
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    # If there are any fields needed add here.

    def __str__(self):
        return self.username


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Project(TimestampModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    code = models.CharField(max_length=64, unique=True, null=False)
    creator = models.ForeignKey(
        Member, on_delete=models.CASCADE, default="", null=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.code, self.title, self.creator)


class Issue(TimestampModel):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    Open = "Open"
    InProgress = "InProgress"
    InReview = "InReview"
    CodeComplete = "CodeComplete"
    QATesting = "QA Testing"
    Done = "Done"
    STATUS = [(Open, Open), (InProgress, InProgress), (InReview, InReview),
              (CodeComplete, CodeComplete), (QATesting, QATesting), (Done, Done)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    type = models.CharField(max_length=8, choices=TYPES,
                            default=BUG, null=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", null=False
    )

    reporter = models.ForeignKey(
        Member, on_delete=models.CASCADE, default="", null=True, related_name='reporter')
    assignee = models.ForeignKey(
        Member, on_delete=models.CASCADE, default="", null=True, related_name='assignee')

    status = models.CharField(max_length=20, choices=STATUS,
                              default=Open, null=False)

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.project, self.title)

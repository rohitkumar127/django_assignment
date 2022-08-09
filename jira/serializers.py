from rest_framework import serializers
from dropship.models import Project, Issue, User, Label, Sprint, Comment, Worklog


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model =Issue
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields="__all__"


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Label
        fields="__all__"

class SprintSerializer(serializers.ModelSerializer):

    class Meta:
        model=Sprint
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields="__all__"
class WorklogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Worklog
        fields="__all__"
from dropship import models
from dropship import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication  # TokenAuthentication ,
from rest_framework.permissions import IsAuthenticated


class MemberModelViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberSerializer


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class IssueModelViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class SprintModelViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

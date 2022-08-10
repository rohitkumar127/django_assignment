from dropship import models
from dropship import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from dropship.permissions import IsAdmin, IsProjectManager, IsProjectManagerOrReadOnly,  SprintUserWritePermission  # Mypermission,


class MemberModelViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'email']


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'code', 'creator', 'creator__email']


class IssueModelViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'type', 'project',
                        'sprint', 'reporter', 'reporter__email', 'assignee__email', 'status', 'labels_list', 'watchers_list__email']


class SprintModelViewSet(viewsets.ModelViewSet):
    queryset = models.Sprint.objects.all()
    serializer_class = serializers.SprintSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsProjectManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'startdate', 'enddate', 'project', 'type']


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment', 'user', 'issue', 'project']

from typing import Generic
from dropship import models
from dropship import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import generics

from dropship.permissions import IsAdmin, IsProjectManager


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
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'type', 'project',
                        'sprint', 'reporter', 'reporter__email', 'assignee__email', 'status', 'labels_list', 'watchers_list__email']

    def update(self, request, pk=None, *args, **kwargs):
        # print(type(request))
        # x = int(args)
        issue_data = self.get_object()  # models.Issue.objects.filter()
        # new_status = self.update_status(
        # issue_data.status, request.data['status']).
        new_status = request.data['status']
        receipents_list = []
        print()
        # print("Sanket Here")
        send_mail(
            'Status Change',
            f'{issue_data.title}- ID:{issue_data.pk}\'s status has been changed from {issue_data.status} to {new_status}',
            'sanketmistry250@gmail.com',
            ['sanketmistry45291@gmail.com'],
            fail_silently=False
        )
        serializer = serializers.IssueSerializer(
            issue_data, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


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

import datetime
import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import viewsets
from dropship.models import Project, Issue, User

from .serializers import ProjectSerializer, LabelSerializer, IssueSerializer, UserSerializer, SprintSerializer, \
    CommentSerializer


# Create your views here.

# class ProjectView(APIView):
#     def get(self,request):
#         id = request.query_params.get('id')
#         if id != None:
#             project = self.get_object(id)
#             response = ProjectSerializer(project)
#         else:
#             projects = Project.objects.all()
#             response = ProjectSerializer(projects, many=True)
#         return Response({"data": response.data})
#
#     def post(self,request):
#         data=request.data
#         serializer=ProjectSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=201)

class ProjectView(viewsets.ViewSet):
    def get_project_by_id(self, request, identifier):
        try:
            queryset = Project.objects.get(pk=identifier)
        except:
            return Response("No project with that Id")
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)


class IssueView(viewsets.ViewSet):
    def get_issue(self, request, identifier):
        try:
            query = Issue.objects.get(pk=identifier)
        except:
            return Response("No project with that Id", status=404)
        response = IssueSerializer(query)
        return Response(response.data, status=200)

    def update_issue(self, request, identifier):
        issue = Issue()
        issue = json.loads(request.body)
        issue_saved = Issue.objects.filter(pk=identifier)
        issue_saved.update(title=issue['title'], description=issue['description']
                           , updated_at=str(datetime.datetime.now(tz=timezone.utc)), type=issue['type'],
                           assignee_id=issue['assignee'], sprint=issue['sprint'])

        issue1=Issue.objects.get(pk=identifier)
        # print('hhh',User.objects.get(pk=1).id)
        for i in issue['watchers']:
            try:
                user=User.objects.get(pk=i)
                issue1.watchers.add(user)
            except:
                return Response("No user with that Id", status=404)
        return Response('Issue updated', status=200)

    def delete(self, request, identifier):
        try:
            Issue.objects.get(pk=identifier).delete()
        except:
            return Response("No project with that Id", status=404)
        return Response('Deleted sucessfully', status=200)

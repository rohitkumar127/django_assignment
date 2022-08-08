import datetime
import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, authentication
from dropship.models import Project, Issue, User, Label
from django.core.mail import send_mail


from .serializers import ProjectSerializer, LabelSerializer, IssueSerializer, UserSerializer, SprintSerializer, \
    CommentSerializer


class ProjectView(viewsets.ViewSet):

    def post(self, request):
        data = request.data
        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def patch(self, request, identifier):
        project = Project.objects.get(pk=identifier)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(data="wrong parameters", status=400)

    def get_project_by_id(self, request, identifier):
        try:
            queryset = Project.objects.get(pk=identifier)
        except:
            return Response("No project with that Id")
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)

    def get_projects(self, request):
        query = Project.objects.all()
        response = ProjectSerializer(query, many=True)
        return Response(response.data)

    def delete(self, request, identifier):
        try:
            Project.objects.get(pk=identifier).delete()
        except:
            return Response("No project with that Id", status=404)
        return Response('Deleted sucessfully', status=200)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class IssueView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_watcher(self, i):
        return User.objects.get()

    def post(self, request):
        data = request.data
        serializer = IssueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request):
        project_id = request.query_params.get('project-id')
        title1 = request.query_params.get('title')
        description1 = request.query_params.get('description')
        if title1 != None and description1 != None:
            response=list(Issue.objects.filter(title=title1))
            response=IssueSerializer(response, many=True)
        elif project_id != None:
            response = list(Issue.objects.filter(project=project_id))
            response = IssueSerializer(response, many=True)
        else:
            query = Issue.objects.all()
            response = IssueSerializer(query, many=True)
        return Response(response.data, status=200)

    def get_issue(self, request, identifier):
        try:
            query = Issue.objects.get(pk=identifier)
        except:
            return Response("No project with that Id", status=404)
        response = IssueSerializer(query)
        return Response(response.data, status=200)

    def update_status(self, from_status=None, to_status=None):
        li = ['open', 'in progress', 'in review', 'code complete ', 'qa testing', 'done']
        from_ind = li.index(from_status)
        try:
            to_ind = li.index(to_status.lower())
        except:
            return False
        if (from_ind == to_ind or from_ind + 1 == to_ind or (from_ind == 2 and to_ind == 0)):
            return True
        else:
            return False

    def patch(self, request, identifier):
        print(type(request))
        issue = Issue.objects.get(pk=identifier)
        status_changeable = self.update_status(issue.status, request.data['status'])
        for i in range(len(request.data['label'])):
            request.data['label'][i]=request.data['label'][i].lower()
        if not status_changeable:
            return Response({"Failed": "Check spelling and sequence of status"}, status=400)
        # send_mail(
        #     f'Status change',
        #     '{issue.title} status has been changed from {issue.status} to {request.data["status"]}',
        #     'az5717@srmist.edu.in',
        #     ['raghavendraarveti@gmail.com'],
        #     fail_silently=False,
        # )
        serializer = IssueSerializer(issue, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
            # return Response(serializer.data, status=201)
        return Response("Issue updated", status=400)

    # def update_issue(self, request, identifier):
    #     issue = Issue()
    #     issue = json.loads(request.body)
    #     issue_saved = Issue.objects.filter(pk=identifier)
    #     issue_saved.update(title=issue['title'], description=issue['description']
    #                        , updated_at=str(datetime.datetime.now(tz=timezone.utc)), type=issue['type'],
    #                        assignee_id=issue['assignee'], sprint=issue['sprint'])
    #
    #     issue1=Issue.objects.get(pk=identifier)
    #     # print('hhh',User.objects.get(pk=1).id)
    #     for i in issue['watchers']:
    #         try:
    #             user=User.objects.get(pk=i)
    #             issue1.watchers.add(user)
    #   token f8b647b75a2882049a582e72d77b13e166bc84bf      except:
    #             return Response("No user with that Id", status=404)
    #     return Response('Issue updated', status=200)

    def attach_label(self,request,identifier):
        # label=LabelSerializer(data=request.data)
        # label.save()
        request.data['label'] = request.data['label'].lower()
        label=request.data['label']
        issue=Issue.objects.get(pk=identifier)
        try:
            issue.label.add(label)
        except:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            issue.label.add(label)
        serializer2=IssueSerializer(issue)
        return Response(serializer2.data, status=201)

    def detach_label(self,request,identifier):
        issue = Issue.objects.get(pk=identifier)
        label=request.data["label"]
        issue.label.remove(label)
        return Response(f"{label} detached from issue")


    def delete(self, request, identifier):
        try:
            Issue.objects.get(pk=identifier).delete()
        except:
            return Response("No issue with that Id", status=404)
        return Response('Deleted sucessfully', status=200)

class LabelView(viewsets.ViewSet):
    def post(self,request):
        request.data['label']=request.data['label'].lower()
        serializer = LabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)

    def delete(self,request,identifier):
        Label.objects.get(pk=identifier.lower()).delete()
        return Response(f"Label {identifier} deleted")
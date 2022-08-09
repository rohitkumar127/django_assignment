import datetime
import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, authentication
from dropship.models import Project, Issue, User, Label, Comment, Sprint, Worklog
from django.core.mail import send_mail
from django.db.models import Q
import sqlite3

from .serializers import ProjectSerializer, LabelSerializer, IssueSerializer, UserSerializer, SprintSerializer, \
    CommentSerializer, WorklogSerializer


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
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(query, request)
        response = ProjectSerializer(result_page, many=True)
        return Response(response.data)

    def delete(self, request, identifier):
        try:
            Project.objects.get(pk=identifier).delete()
        except:
            return Response("No project with that Id", status=404)
        return Response('Deleted sucessfully', status=200)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
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
        dsql = request.query_params.get('dsql')
        if dsql != None:
            connection = sqlite3.connect('db.sqlite3')
            crsr = connection.cursor()
            sql_command = 'select id from dropship_issue where'+dsql
            crsr.execute(sql_command)
            p = crsr.fetchall()
            print(crsr.fetchall())
            l = []
            for i in p:
                print('123', i)
                issue = Issue.objects.get(pk=i[0])
                l.append(issue)
                print('abc', i)
            response=IssueSerializer(l,many=True)
            # keys=('id','created_at','updated_at','title','description','status','type','project','reporter')
            crsr.close()
            return Response({'data':response.data})
        project_id = request.query_params.get('project-id')
        title1 = request.query_params.get('title')
        description1 = request.query_params.get('description')
        if title1 != None and description1 != None:
            response = list(Issue.objects.filter(title=title1, description=description1))
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(response, request)
            response = IssueSerializer(result_page, many=True)
        elif project_id != None:
            response = list(Issue.objects.filter(project=project_id))
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(response, request)
            response = IssueSerializer(result_page, many=True)
        else:
            print('bbb')
            query = Issue.objects.all()
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(query, request)
            response = IssueSerializer(result_page, many=True)
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
            request.data['label'][i] = request.data['label'][i].lower()
        if not status_changeable:
            return Response({"Failed": "Check spelling and sequence of status"}, status=400)
        # send_mail(
        #     'Status change',
        #     f'{issue.title} status has been changed from {issue.status} to {request.data["status"]}',
        #     'az5717@srmist.edu.in',
        #     ['raghavendraarveti@gmail.com'],
        #     fail_silently=False,
        # )
        serializer = IssueSerializer(issue, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        # return Response(serializer.data, status=201)
        return Response("Issue updated", status=200)

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

    def attach_label(self, request, identifier):
        # label=LabelSerializer(data=request.data)
        # label.save()
        request.data['label'] = request.data['label'].lower()
        label = request.data['label']
        issue = Issue.objects.get(pk=identifier)
        try:
            issue.label.add(label)
        except:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            issue.label.add(label)
        serializer2 = IssueSerializer(issue)
        return Response(serializer2.data, status=201)

    def detach_label(self, request, identifier):
        issue = Issue.objects.get(pk=identifier)
        label = request.data["label"]
        issue.label.remove(label)
        return Response(f"{label} detached from issue")

    def delete(self, request, identifier):
        try:
            Issue.objects.get(pk=identifier).delete()
        except:
            return Response("No issue with that Id", status=404)
        return Response('Deleted sucessfully', status=200)


class LabelView(viewsets.ViewSet):
    def post(self, request):
        request.data['label'] = request.data['label'].lower()
        serializer = LabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def delete(self, request, identifier):
        Label.objects.get(pk=identifier.lower()).delete()
        return Response(f"Label {identifier} deleted")


class CommentView(viewsets.ViewSet):
    def post(self, request):
        data = request.data
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def patch(self, request, identifier):
        data = request.data['comment']
        comment = Comment.objects.get(pk=identifier)
        if int(request.query_params.get('logged-user-id')) == comment.user_id:
            comment.comment = data
            comment.save()
            return Response(data="Comment updated", status=200)
        return Response(data="Only commented user can edit", status=400)

    def delete(self, request, identifier):
        try:
            comment = Comment.objects.get(pk=identifier)
            if int(request.query_params.get('logged-user-id')) == comment.user_id:
                comment.delete()
            else:
                return Response(data="Only commented user can delete his own comment", status=400)
        except:
            return Response(data="No comment with that Id", status=400)
        return Response(data="Comment deleted", status=200)


class SprintView(viewsets.ViewSet):
    def post(self, request):
        data = request.data
        serializer = SprintSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def start_stop_sprint(self, request, identifier):
        sprint = Sprint.objects.get(pk=identifier)
        if sprint.sprint_status == None:
            sprint.sprint_status = True
            sprint.start_date = datetime.date.today()
            response = "Sprint started"
        elif sprint.sprint_status == True:
            sprint.sprint_status = False
            sprint.end_date = datetime.date.today()
            response = "Sprint stoped"
        else:
            response = "Sprint once stopped can not be started"
            return Response(response, status=400)
        sprint.save()
        return Response(response, status=200)

    def delete(self, request, identifier):
        try:
            Sprint.objects.get(pk=identifier).delete()
        except:
            return Response(data="No sprint with that Id", status=400)
        return Response(data="Sprint deleted", status=200)

    def add_issue_to_sprint(self, request, identifier):
        issue_id = request.query_params.get('issue-id')
        if issue_id == None:
            return Response("Please pass issue-id as query param", status=400)
        try:
            issue = Issue.objects.get(pk=issue_id)
        except:
            return Response("No such issue exists", status=400)
        issue.sprint_id = identifier
        return Response(data="Issue added to sprint", status=200)

    def remove_issue_from_sprint(self, request, identifier):
        issue_id = request.query_params.get('issue-id')
        if issue_id == None:
            return Response("Please pass issue-id as query param", status=400)
        try:
            issue = Issue.objects.get(pk=issue_id)
        except:
            return Response("No such issue exists", status=400)
        issue.sprint_id = None
        return Response(data="Issue removed from sprint", status=200)


class WorklogView(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        serializer = WorklogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def patch(self, request, identifier):
        worklog = Worklog.objects.get(pk=identifier)
        if int(request.query_params.get('logged-user-id')) == worklog.user_id:
            try:
                if (request.data['user'] != worklog.user) or (request.data['issue'] != worklog.issue):
                    return Response(data="Issue and user can not be edited", status=400)
            except KeyError:
                pass
            serializer = WorklogSerializer(worklog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(data="wrong parameters", status=400)
        return Response(data="You can edit only your log", status=400)

    def delete(self, request, identifier):
        try:
            worklog = Worklog.objects.get(pk=identifier)
            if int(request.query_params.get('logged-user-id')) == worklog.user_id:
                worklog.delete()
            else:
                return Response(data="You can edit only your log", status=400)
        except:
            Response("Worklog not found", status=400)
        return Response("Worklog deleted", status=200)

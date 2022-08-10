import datetime

from django.shortcuts import render
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, authentication
from dropship.models import Project, Issue, User, Label, Comment, Sprint, Worklog,IssueWatcher
from django.core.mail import send_mail
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
        title1 = request.query_params.get('title')
        description1 = request.query_params.get('description')
        creator1 = request.query_params.get('creator')
        response = Project.objects
        print(title1)
        if title1:
            response = response.filter(title=title1)
        if description1:
            response = response.filter(description=description1)
        if creator1:
            response = response.filter(creator=creator1)
        paginator = LimitOffsetPagination()
        try:
            result_page = paginator.paginate_queryset(response, request)
        except TypeError:
            response = response.all()
            result_page = paginator.paginate_queryset(response, request)
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
            print(12,dsql)
            sql_command = 'select * from dropship_issue where '+dsql
            crsr.execute(sql_command)
            p = crsr.fetchall()
            print(p)
            l = []
            for i in p:
                issue = Issue.objects.get(pk=i[0])
                l.append(issue)
            response = IssueSerializer(l, many=True)
            # keys=('id','created_at','updated_at','title','description','status','type','project','reporter')
            crsr.close()
            return Response({'data': response.data}, status=200)

        title1 = request.query_params.get('title')
        description1 = request.query_params.get('description')
        reporter1 = request.query_params.get('reporter')
        assignee1 = request.query_params.get('assignee')
        status1 = request.query_params.get('status')
        type1 = request.query_params.get('type')
        sprint1 = request.query_params.get('sprint')
        # label1=request.query_params.get('label')
        project1 = request.query_params.get('project')
        # watcher1=request.query_params.get('watchers')
        response = Issue.objects
        if title1:
            response = response.filter(title=title1)
        if description1:
            response = response.filter(description=description1)
        if reporter1:
            response = response.filter(reporter=reporter1)
        if assignee1:
            response = response.filter(assignee=assignee1)
        if status1:
            response = response.filter(status=status1)
        if type1:
            response = response.filter(type=type1)
        if sprint1:
            response = response.filter(sprint=sprint1)
        if project1:
            response = response.filter(project=project1)
        paginator = LimitOffsetPagination()
        try:
            result_page = paginator.paginate_queryset(response, request)
        except TypeError:
            response = response.all()
            result_page = paginator.paginate_queryset(response, request)
        response = IssueSerializer(result_page, many=True)
        return Response(response.data, status=200)

    def get_issue(self, request, identifier):
        try:
            query = Issue.objects.get(pk=identifier)
            # query=IssueSerializer(query)
            # print(query.watchers.all())
        except:
            return Response("No issue with that Id", status=404)
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

    # def mailing(self,identifier):


    def patch(self, request, identifier):
        print(type(request))
        issue = Issue.objects.get(pk=identifier)
        try:
            status_changeable = self.update_status(issue.status, request.data['status'])
            if not status_changeable:
                return Response({"Failed": "Check spelling and sequence of status"}, status=400)
            if not issue.status==request.data['status']:
                mail_ids=list(map(lambda i:i.email,issue.watchers.all()))
                print(mail_ids)
                send_mail(
                    'Status change',
                    f'{issue.title} status has been changed from {issue.status} to {request.data["status"]}',
                    'az5717@srmist.edu.in',
                    mail_ids,
                    fail_silently=False,
                )
        except KeyError:
            pass
        try:
            for i in range(len(request.data['label'])):
                request.data['label'][i] = request.data['label'][i].lower()
        except KeyError:
            pass

        serializer = IssueSerializer(issue, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        # return Response(serializer.data, status=201)
        return Response("Issue updated", status=200)

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

    def add_watcher(self,request,identifier):
        watcher=request.query_params.get('watcher-id')
        issue=Issue.objects.get(pk=identifier)
        watcher=User.objects.get(pk=watcher)
        issue.watchers.add(watcher.email)
        issue.save()
        return Response(data="Watcher added")

    def remove_watcher(self,request,identifier):
        watcher = request.query_params.get('watcher-id')
        issue = Issue.objects.get(pk=identifier)
        watcher = User.objects.get(pk=watcher)
        issue.watchers.remove(watcher)
        issue.save()
        return Response(data="Watcher Removed")

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

    def get(self, request):
        try:
            response = Label.objects.get(pk=request.query_params.get('label'))
            response = LabelSerializer(response)
        except:
            response = Label.objects.all()
            response = LabelSerializer(response, many=True)
        return Response(response.data, status=200)


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

    def get(self, request):
        user = request.query_params.get('user')
        issue = request.query_params.get('issue')
        comment = request.query_params.get('comment')
        response = Comment.objects
        if user:
            response = response.filter(user=user)
        if comment:
            response = response.filter(comment=comment)
        if issue:
            response = response.filter(issue=issue)
        paginator = LimitOffsetPagination()
        try:
            result_page = paginator.paginate_queryset(response, request)
        except TypeError:
            response = response.all()
            result_page = paginator.paginate_queryset(response, request)
        response = CommentSerializer(result_page, many=True)
        return Response(response.data)


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

    def get(self, request):
        sprint_title = request.query_params.get('sprint-title')
        start_date = request.query_params.get('start-date')
        end_date = request.query_params.get('end-date')
        sprint_status = request.query_params.get('sprint-status')
        project = request.query_params.get('project')
        response = Sprint.objects
        if sprint_status:
            response = response.filter(sprint_status=sprint_status)
        if sprint_title:
            response = response.filter(sprint_title=sprint_title)
        if start_date:
            response = response.filter(start_date=start_date)
        if end_date:
            response = response.filter(end_date=end_date)
        if project:
            response = response.filter(project=project)
        paginator = LimitOffsetPagination()
        try:
            result_page = paginator.paginate_queryset(response, request)
        except TypeError:
            response = response.all()
            result_page = paginator.paginate_queryset(response, request)
        response = SprintSerializer(result_page, many=True)
        return Response(response.data)


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

    def get(self, request):
        time_spent = request.query_params.get('time-spent')
        start_date = request.query_params.get('start-date')
        remaining_estimation = request.query_params.get('remaining-estimation')
        work_description = request.query_params.get('work-description')
        issue = request.query_params.get('issue')
        user = request.query_params.get('user')
        response = Worklog.objects
        if time_spent:
            response = response.filter(time_spent=time_spent)
        if start_date:
            response = response.filter(start_date=start_date)
        if remaining_estimation:
            response = response.filter(remaining_estimation=remaining_estimation)
        if work_description:
            response = response.filter(work_description=work_description)
        if issue:
            response = response.filter(issue=issue)
        if user:
            response = response.filter(user=user)
        paginator = LimitOffsetPagination()
        try:
            result_page = paginator.paginate_queryset(response, request)
        except TypeError:
            response = response.all()
            result_page = paginator.paginate_queryset(response, request)
        response = WorklogSerializer(result_page, many=True)
        return Response(response.data)

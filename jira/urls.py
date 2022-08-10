from django.urls import path
from .views import ProjectView, IssueView, CustomAuthToken, LabelView, CommentView, SprintView, WorklogView
from rest_framework.authtoken import views
urlpatterns = [
path("projects/<int:identifier>", ProjectView.as_view({'get': 'get_project_by_id'})),
path("projects", ProjectView.as_view({'get': 'get_projects'})),
path("issue/<int:identifier>",IssueView.as_view({'get':'get_issue','delete':'delete'})),
path("issues",IssueView.as_view({'get':'get'})),
path("issue/<int:identifier>/add-watcher",IssueView.as_view({'patch':'add_watcher'})),
path("issue/<int:identifier>/remove-watcher",IssueView.as_view({'patch':'remove_watcher'})),
path('api-token-auth', CustomAuthToken.as_view()),
path('issue/<int:identifier>/attach-label',IssueView.as_view({'patch':'attach_label'})),
path('label',LabelView.as_view({'post':'post'})),
path('label/<str:identifier>',LabelView.as_view({'delete':'delete'})),
path('issue/<int:identifier>/detach-label',IssueView.as_view({'delete':'detach_label'})),
path('issue/comment',CommentView.as_view({'post':'post'})),
path('issue/comment/<int:identifier>',CommentView.as_view({'patch':'patch'})),
path('sprint',SprintView.as_view({'post':'post'})),
path('sprint/<int:identifier>/start-stop',SprintView.as_view({'patch':'start_stop_sprint'})),
path('sprint/<int:identifier>',SprintView.as_view({'delete':'delete'})),
path('sprint/<int:identifier>/add-issue',SprintView.as_view({'patch':'add_issue_to_sprint'})),
path('sprint/<int:identifier>/remove-issue',SprintView.as_view({'patch':'remove_issue_from_sprint'})),
path('worklog',WorklogView.as_view({'post':'create'})),
path('worklog/<int:identifier>',WorklogView.as_view({'patch':'patch'}))
]
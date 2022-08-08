from django.urls import path
from .views import ProjectView,IssueView,CustomAuthToken,LabelView
from rest_framework.authtoken import views
urlpatterns = [
path("projects/<int:identifier>", ProjectView.as_view({'get': 'get_project_by_id'})),
path("projects", ProjectView.as_view({'get': 'get_projects'})),
path("issue/<int:identifier>",IssueView.as_view({'get':'get_issue','delete':'delete'})),
path("issues/",IssueView.as_view({'get':'get'})),
path('api-token-auth', CustomAuthToken.as_view()),
path('issue/<int:identifier>/attach-label',IssueView.as_view({'patch':'attach_label'})),
path('label',LabelView.as_view({'post':'post'})),
path('label/<str:identifier>',LabelView.as_view({'delete':'delete'})),
path('issue/<int:identifier>/detach-label',IssueView.as_view({'delete':'detach_label'})),
]
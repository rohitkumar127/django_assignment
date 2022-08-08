from django.urls import path
from .views import ProjectView,IssueView

urlpatterns = [
path("projects/<int:identifier>", ProjectView.as_view({'get': 'get_project_by_id'})),
path("issue/<int:identifier>",IssueView.as_view({'get':'get_issue','delete':'delete','put':'update_issue'})),

]
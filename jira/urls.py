from django.urls import path
from .views import ProjectView

urlpatterns = [
path("projects/", ProjectView.as_view({'get': 'abc','post': 'createProject'}))
]
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dropship import views
from rest_framework import viewsets
from dropship.auth import CustomAuthToken


router = DefaultRouter()
# router.register('owners',  views.OwnerView)
router.register('projects', views.ProjectModelViewSet, basename='project')
router.register('members', views.MemberModelViewSet, basename='member')
router.register('issue', views.IssueModelViewSet, basename='issue')
router.register('sprint', views.SprintModelViewSet, basename='sprint')
router.register('comment', views.CommentModelViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
# from rest_framework.views import APIView
from dropship.models import Project, Issue, User
from .serializers import ProjectSerializer


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
    def abc(self, request):
        queryset=Project.objects.all()
        serializer=ProjectSerializer(queryset,many=True)
        return Response(serializer.data)

    def createProject(self, request):
        data=request.data
        serializer=ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)

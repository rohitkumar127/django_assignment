# from urllib import request
from dropship import models
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
# from rest_framework.response import Response


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Member
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):

        user = models.User.objects.create_user(
            validated_data['email'], validated_data['email'], validated_data['password'])
        # print(user)
        member = models.Member.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            user=user
        )
        return member

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        obj = models.Member.objects.get(id=instance.id)

        return super().update(obj, validated_data)


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Label
        fields = "__all__"


class IssueSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    labels_list = LabelSerializer(many=True)
    watchers_list = MemberSerializer(many=True)

    class Meta:
        model = models.Issue
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        labels_data = validated_data.pop('labels_list')
        watchers_data = validated_data.pop('watchers_list')
        album = models.Issue.objects.create(**validated_data)

        temp_list = []
        temp_list1 = []
        for label_data in labels_data:
            obj = models.Label.objects.create(**label_data)
            temp_list.append(obj)

        for watcher_data in watchers_data:
            obj = models.Member.objects.create(**watcher_data)
            temp_list1.append(obj)

        album.labels_list.add(*temp_list)
        album.watchers_list.add(*temp_list1)
        # album.add(new_timelog)
        return album


class SprintSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sprint
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = "__all__"

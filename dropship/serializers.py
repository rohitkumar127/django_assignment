from dropship import models
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = models.Member
    #     fields = "__all__"

    class Meta:
        model = models.Member
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):

        user = models.User.objects.create_user(
            validated_data['email'], validated_data['email'], validated_data['password'])

        member = models.Member.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
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


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Issue
        fields = "__all__"

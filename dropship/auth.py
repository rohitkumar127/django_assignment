
from rest_framework.response import Response

from dropship import models
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CustomAuthToken(ObtainAuthToken):

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        try:
            member_obj = models.Member.objects.get(user=user.pk)
        except:
            print("User Doesn't Exist")
        return Response({
            'token': token.key,
            'user_id': member_obj.pk,
            'member_id': member_obj.id,
            'email': member_obj.email,
            'first_name': member_obj.first_name,
            'last_name': member_obj.last_name,
        })

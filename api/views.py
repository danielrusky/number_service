from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer
from api.services import UserLoginService, UserVerifyService
from users.models import User


class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'


class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        UserLoginService(
            phone=request.POST.get("phone")
        ).execute()
        return Response(
            {
                'detail': 'OK'
            },
            status=status.HTTP_200_OK
        )


class UserVerifyAPIView(APIView):

    def post(self, request, *args, **kwargs):
        UserVerifyService(
            phone=request.POST.get("phone"),
            code=request.POST.get("code"),
        ).execute()
        return Response(
            {
                'detail': 'OK'
            },
            status=status.HTTP_200_OK
        )

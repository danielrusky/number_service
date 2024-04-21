from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer
from api.services import UserLoginService, UserVerifyService, UserInviteCodeService
from users.models import User


# этот класс, который отвечает за просмотр профиля определенного пользователя
class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'


# этот класс, который отвечает за обработку логмина пользователя
class UserLoginAPIView(APIView):

    # метод отвечающий за обработку пост запроса
    def post(self, request, *args, **kwargs):
        UserLoginService(
            phone=request.POST.get("phone")
        ).execute()
        return Response(
            {
                'detail': 'Код отправлен на номер телефона.'
            },
            status=status.HTTP_200_OK
        )


# этот код отвечает за верификацию пользователя
class UserVerifyAPIView(APIView):

    def post(self, request, *args, **kwargs):
        result = UserVerifyService(
            phone=request.POST.get("phone"),
            code=request.POST.get("code"),
        ).execute()
        return Response(
            {
                'token': result
            },
            status=status.HTTP_200_OK
        )


# класс, который отвечает за подписку на другого пользователя
class UserInviteCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # метод отвечающий за обработку пост запроса
    def post(self, request, *args, **kwargs):
        UserInviteCodeService(
            user=request.user,
            invite_code=request.POST.get("invite_code")
        ).execute()
        return Response(
            {
                'detail': 'Вы успешно подписались.'
            },
            status=status.HTTP_200_OK
        )

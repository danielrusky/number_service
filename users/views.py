import os

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import AuthenticationForm
from users.models import User
from users.tasks import send_verify_code_for_number
from users.validators import generate_unique_invite_code


class HomePageView(TemplateView):
    template_name = 'users/index.html'


class UserLoginView(CreateView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:login_verify')

    def form_valid(self, form):
        if form.is_valid():
            user = User.objects.filter(phone=form.cleaned_data['phone']).first()
            if not user:
                user = form.save(commit=False)
                invite_code = generate_unique_invite_code(6)
                user.invite_code = invite_code
                user.save()

            # Тут логика отправки кода из 4 символов
            send_verify_code_for_number.apply_async(
                (user.id,),
                countdown=os.getenv(
                    'COUNTDOWN_SEND_CODE',
                    default=5
                )
            )
            self.request.COOKIES['user_id'] = user.id
        return redirect(self.success_url)


class UserVerifyView(TemplateView):
    template_name = 'users/verify.html'

    def post(self, request, *args, **kwargs):
        pass

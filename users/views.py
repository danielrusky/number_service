from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import AuthenticationForm
from users.models import User
from users.validators import generate_unique_invite_code


class HomePageView(TemplateView):
    template_name = 'users/index.html'


class UserLoginView(CreateView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:login_verify')

    def form_valid(self, form):
        if form.is_valid():
            if not User.objects.filter(phone=form.cleaned_data['phone']):
                user = form.save(commit=False)
                invite_code = generate_unique_invite_code(6)
                user.invite_code = invite_code
                user.save()

            # Тут логика отправки кода из 4 символов
        return redirect(self.success_url)


class UserVerifyView(TemplateView):
    template_name = 'users/verify.html'

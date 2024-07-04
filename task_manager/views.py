from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import redirect, render   # noqa f401
from django.views import View
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, 'index.html', context={})


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('You have successfully logged in.')
        )
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.INFO,
            _('You have successfully logged out.')
        )
        return super().dispatch(request, *args, **kwargs)

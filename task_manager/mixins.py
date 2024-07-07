from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class LoginRequiredMixinWithFlash(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _('You are not authorized! Please log in')
        )
        return redirect('login')


class UserIsSelfMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _('You do not have permission to change another user')
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

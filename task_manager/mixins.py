from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class LoginRequiredAndUserIsSelfMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect):
            messages.add_message(
                request,
                messages.ERROR,
                _('You are not authorized! Please log in')
            )
            return response

        user_id = kwargs.get('pk')
        if user_id != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _('You do not have permission to change another user')
            )
            return redirect('users')

        return response

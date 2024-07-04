from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views import View


class LoginRequiredAndUserIsSelfMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                _('You are not authorized! Please log in')
            )
            return redirect('login')

        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.add_message(
                request,
                messages.ERROR,
                _('You do not have permission to change another user')
            )
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)

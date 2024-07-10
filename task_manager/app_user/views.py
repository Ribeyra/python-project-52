from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash, \
    ObjectPermissionMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CreateUser(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UpdateUser(
    LoginRequiredMixinWithFlash,
    ObjectPermissionMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    permission_error_message = _(
        'You do not have permission to change another user'
    )


class DeleteUser(
    LoginRequiredMixinWithFlash,
    ObjectPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'users/delete.html'
    model = get_user_model()
    success_url = reverse_lazy('users')
    success_message = _('User deleted successfully')
    permission_error_message = _(
        'You do not have permission to change another user'
    )

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _('Cannot delete user because it is in use')
            )
            return redirect(self.success_url)


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_queryset(self):
        return self.model.objects.values(
            'id', 'first_name', 'last_name', 'username', 'date_joined'
        ).order_by('id')

from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash, \
    ObjectPermissionMixin, ProtectedErrorHandlingMixin
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
    ProtectedErrorHandlingMixin,
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
    protected_error_message = _('Cannot delete user because it is in use')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
    context_object_name = 'users'

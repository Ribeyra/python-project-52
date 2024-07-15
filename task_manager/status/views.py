from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash, \
    ProtectedErrorHandlingMixin
from .models import Status
from .forms import StatusCreationForm


class CreateStatus(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'statuses/create.html'
    form_class = StatusCreationForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')


class UpdateStatus(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    UpdateView
):
    model = Status
    form_class = StatusCreationForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class DeleteStatus(
    LoginRequiredMixinWithFlash,
    ProtectedErrorHandlingMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status deleted successfully')
    protected_error_message = _('Cannot delete status because it is in use')


class StatusListView(LoginRequiredMixinWithFlash, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

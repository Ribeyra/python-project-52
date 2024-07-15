from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash
from .models import Label
from .forms import LabelCreationForm


class CreateLabel(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'labels/create.html'
    form_class = LabelCreationForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')


class UpdateLabel(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    form_class = LabelCreationForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class DeleteLabel(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label deleted successfully')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверяем, используется ли метка в задачах
        if self.object.task_labels.all().exists():
            messages.error(
                request,
                _('Cannot remove label because it is in use')
            )
            return redirect(self.success_url)
        # Если метка не используется в задачах, удаляем её
        return super().post(request, *args, **kwargs)


class LabelListView(LoginRequiredMixinWithFlash, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash
from .models import Tag
from .forms import TagCreationForm


class CreateTag(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'tags/create.html'
    form_class = TagCreationForm
    success_url = reverse_lazy('tags')
    success_message = _('Tag successfully created')


class UpdateTag(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    UpdateView
):
    model = Tag
    form_class = TagCreationForm
    template_name = 'tags/update.html'
    success_url = reverse_lazy('tags')
    success_message = _('Tag successfully updated')


class DeleteTag(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'tags/delete.html'
    model = Tag
    success_url = reverse_lazy('tags')
    success_message = _('Tag deleted successfully')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверяем, используется ли метка в задачах
        if self.object.task_tags.all().exists():
            messages.error(
                request,
                _('Cannot remove tag because it is in use')
            )
            return redirect(self.success_url)
        # Если метка не используется в задачах, удаляем её
        return super().post(request, *args, **kwargs)


class TagListView(LoginRequiredMixinWithFlash, ListView):
    model = Tag
    template_name = 'tags/index.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return self.model.objects.values(
            'id', 'name', 'description', 'created_at'
        ).order_by('id')

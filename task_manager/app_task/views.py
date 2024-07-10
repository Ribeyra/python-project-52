from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, \
    ListView, DetailView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMixinWithFlash, \
    ObjectPermissionMixin
from .models import Task
from .forms import TaskCreationForm


class CreateTask(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'tasks/create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(
    LoginRequiredMixinWithFlash,
    SuccessMessageMixin,
    UpdateView
):
    model = Task
    form_class = TaskCreationForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')


class DeleteTask(
    LoginRequiredMixinWithFlash,
    ObjectPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task deleted successfully')

    object_attr = 'author'
    permission_error_message = _('Only its author can delete a task')


class TaskListView(LoginRequiredMixinWithFlash, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.select_related(
            'status',
            'author',
            'assignee'
        ).values(
            'id',
            'title',
            'status__name',
            'author__username',
            'assignee__username',
            'created_at'
        ).order_by('id')


class TaskDetailView(LoginRequiredMixinWithFlash, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

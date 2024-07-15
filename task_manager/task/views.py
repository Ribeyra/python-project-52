from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from task_manager.mixins import LoginRequiredMixinWithFlash, \
    ObjectPermissionMixin
from .filters import TaskFilter
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


class TaskListView(LoginRequiredMixinWithFlash, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_queryset(self):
        return self.model.objects.select_related(
            'status',
            'author',
            'executor'
        ).all()

    def get_filterset(self, filterset_class):
        return filterset_class(
            data=self.request.GET or None,
            request=self.request,
            queryset=self.get_queryset()
        )


class TaskDetailView(LoginRequiredMixinWithFlash, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

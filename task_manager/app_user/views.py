from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredAndUserIsSelfMixin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CreateUser(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('User successfully registered')
        )
        return super().form_valid(form)


class UpdateUser(LoginRequiredAndUserIsSelfMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('User successfully updated')
        )
        return super().form_valid(form)

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('id')
        return get_object_or_404(User, id=user_id)


class DeleteUser(LoginRequiredAndUserIsSelfMixin, DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('User deleted successfully')
        )
        return response

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('id')
        return get_object_or_404(User, id=user_id)


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    queryset = User.objects.values(
        'id',
        'first_name',
        'last_name',
        'username',
        'date_joined'
    ).order_by('id')

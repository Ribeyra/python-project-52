from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CreateUser(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(request, 'users/create.html', {'form': form})


class UpdateUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']
        user = get_object_or_404(User, id=user_id)
        form = CustomUserChangeForm(instance=user)
        return render(
            request,
            'users/update.html',
            {'form': form, 'id': user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs['id']
        user = get_object_or_404(User, id=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        return render(
            request,
            'users/update.html',
            {'form': form, 'id': user_id}
        )

    # def post(self, request, *args, **kwargs):
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('users')
    #     return render(request, 'users/update.html', {'form': form, 'id': id})


def users(request):
    users = User.objects.values(
        'id', 'first_name', 'last_name', 'username', 'date_joined'
    ).all()
    return render(request, 'users/index.html', context={'users': users})

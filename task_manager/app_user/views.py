from django.shortcuts import render
from django.views import View
from task_manager.app_user.models import User


class CreateUser(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/create_user.html', {})

    """ def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        # Если данные корректные, то сохраняем данные формы
        if form.is_valid():
            form.save()
            # Редирект на указанный маршрут
            return redirect('index')
        # Если данные некорректные, то возвращаем человека обратно на
        # страницу с заполненной формой
        return render(request, 'login.html', {'form': form}) """


def users(request):
    users = User.objects.values(
        'id', 'first_name', 'last_name', 'username', 'date_joined'
    ).all()
    return render(request, 'users/users.html', context={'users': users})

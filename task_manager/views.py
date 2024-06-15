from django.shortcuts import redirect, render   # noqa f401
from django.views import View


def index(request):
    return render(request, 'index.html', context={})


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})

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


class CreateUser(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_user.html', {})

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
    return render(request, 'users.html', context={})

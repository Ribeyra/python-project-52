from django.utils import translation


def current_language(request):
    return {
        'LANGUAGE_CODE': translation.get_language(),
    }

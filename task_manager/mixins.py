from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class LoginRequiredMixinWithFlash(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            _('You are not authorized! Please log in')
        )
        return redirect('login')


class ObjectPermissionMixin:
    """
    Mixin to enforce object-level permissions based on a user attribute.

    Attributes:
        object_attr (str): The attribute of the object that should be compared
            to the user. Defaults to 'id'.
        success_url (str): The URL to redirect to if the permission check
            fails. Defaults to 'index'.
        permission_error_message (str): The error message to display if the
            permission check fails. Defaults to 'You do not have permission to
            perform this action.'.

    Methods:
        dispatch(request, *args, **kwargs):
            Override the default dispatch method to enforce the permission
            check. If the user does not have permission, add an error message
            and redirect to the success URL.

        add_flash_and_redirect(request):
            Add an error message to the messages framework and redirect to the
            success URL.
    """
    object_attr = 'id'
    success_url = 'index'
    permission_error_message = _(
        'You do not have permission to perform this action.'
    )

    def dispatch(self, request, *args, **kwargs):
        """
        Override the default dispatch method to enforce the permission check.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: A redirect response if the permission check fails,
            or the result of the superclass dispatch method if it passes.
        """
        obj = self.get_object()
        obj_user_attr = getattr(obj, self.object_attr)
        user = request.user

        if isinstance(obj_user_attr, int):
            if obj_user_attr != getattr(user, 'id'):
                return self.add_flash_and_redirect(request)
        else:
            if getattr(obj_user_attr, 'id') != getattr(user, 'id'):
                return self.add_flash_and_redirect(request)

        return super().dispatch(request, *args, **kwargs)

    def add_flash_and_redirect(self, request):
        """
        Add an error message to the messages framework and redirect to the
        success URL.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A redirect response to the success URL.
        """
        messages.add_message(
            request,
            messages.ERROR,
            self.permission_error_message
        )
        return redirect(self.success_url)


class ProtectedErrorHandlingMixin:
    success_url = 'index'
    protected_error_message = _(
        'Cannot delete this object because it is in use'
    )

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            return redirect(self.success_url)

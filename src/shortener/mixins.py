from django.contrib.auth.mixins import LoginRequiredMixin


class StaffMixin(LoginRequiredMixin):
    permission_denied_message = "This action is for staff only."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

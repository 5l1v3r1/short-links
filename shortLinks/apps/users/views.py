from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    """
    User registration
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = reverse_lazy('main:index')
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

from django.contrib import auth
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from OpportunityHub.accounts.forms import RegisterUserForm, LoginForm, ChangePassword
from OpportunityHub.accounts.signals import create_user_profile
from OpportunityHub.core.accounts_mixins import RedirectAuthenticatedUserMixin

userModel = get_user_model()


class RegisterView(RedirectAuthenticatedUserMixin, CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login_redirect_dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


@login_required(login_url='login')
def singout(request):
    auth.logout(request)
    return redirect('index')


class LoginUserView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class ChangePass(PasswordChangeView):
    form_class = ChangePassword
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy('login_redirect_dashboard')


class RedirectDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_type = request.user.role

        if user_type == 'company':
            return redirect('company-dashboard')
        elif user_type == 'candidate':
            return redirect('job seeker dashboard')
        else:
            return redirect('select_role')  # Redirect to a default page if the role is not recognized


def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')  # Assuming you have a form field named 'role' for role selection
        if role:
            # Update the user's role
            request.user.role = role
            request.user.save()
            create_user_profile(sender=userModel, instance=request.user, created=True)
            return redirect('login_redirect_dashboard')

    return render(request, 'select_role.html')

from django.contrib import auth, messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_text)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, FormView, RedirectView

from accounts.forms import *
from accounts.models import User
from django.urls import reverse_lazy
from .forms import JobseekskilsFormset
from django.db import transaction


class RegisterJobSeeker(CreateView):
    model = User
    success_message = 'Your Account has been created sucessfully!'
    success_url = reverse_lazy('accounts:login')
    template_name = "accounts/employee/register.html"
    form_class=EmployeeRegistrationForm
    def get_context_data(self, **kwargs):
        data = super(RegisterJobSeeker, self).get_context_data(**kwargs)
        if self.request.POST:
            data['addskills'] = JobseekskilsFormset(self.request.POST)
        else:
            data['addskills'] = JobseekskilsFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        addskills = context['addskills']
        
        with transaction.atomic():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            self.object = form.save()

            if addskills.is_valid():
                addskills.instance = self.object
                addskills.save()
        return super(RegisterJobSeeker, self).form_valid(form)


class RegisterEmployerView(CreateView):
    model = User
    success_message = 'Your Account has been created sucessfully!'
    form_class = EmployerRegistrationForm
    template_name = "accounts/employer/register.html"
    success_url = "/"
    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES )
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/employer/register.html", {"form": form})


class LoginView(FormView):
    """
    Provides the ability to login as a user with an email and password
    """
    success_url = "/"
    form_class = UserLoginForm
    template_name = "accounts/login.html"
    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"] != "":
            return self.request.GET["next"]
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        if self.request.user.role=="employer":
            return redirect('jobs:employer-dashboard')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = "/"

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return super(LogoutView, self).get(request, *args, **kwargs)
    
#reset password functionalities
def RequestResetEmail(request):
    if request.method == 'POST':
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email)
            if user.exists():
                uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
                domain = get_current_site(request).domain #gives us the domain
                link = reverse('accounts:reset-password', 
                                kwargs={
                                    'uidb64':uidb64, 
                                    'token':PasswordResetTokenGenerator().make_token(user[0])
                                        })
                reset_password_url = f"http://{domain+link}"
                
                mail_subject = "Reset Password"

                
                mail_body = f"hi click the link below to reset your password\n {reset_password_url}"
                mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
                messages.success(request, "Check your Email for the reset link")
                return redirect('accounts:login')
            else:
                messages.error(request, "Sorry, there is no user with that email")
                return redirect('accounts:request-reset-email')
    form = ResetEmailForm()
    return render(request, 'accounts/reset_email_form.html', {'form':form})
  
def ResetPasswordView(request, uidb64, token): 
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            context = {
                'uidb64':uidb64,
                'token':token,
            }
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password1']
            if password1 == "":
                messages.error(request, "Password is required")
            if password2 == "":
                messages.error(request, "Repeat Password is required")
                return render(request, 'accounts/reset_password.html', context)
            if password1 != password2:
                messages.error(request, "Passwords do not match")
            if len(password1)<6:
                messages.error(request,"Password is too short")
                return render(request, 'accounts/reset_password.html', context)
            if password1 != password2:
                messages.error(request, "Passwords do not match")
            if len(password1)<6:
                messages.error(request,"Password is too short")
                return render(request, 'accounts/reset_password.html', context)  
            
            try:
                user_id = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
                user.set_password(password1)
                user.save()
                messages.success(request, "password changed successfully")
                return redirect('accounts:login')
            except DjangoUnicodeDecodeError as identifier:
                messages.error(request, "oops! something went wrong")
                return render(request, 'accounts/reset_password.html', context)
        
    context = {
        'uidb64':uidb64, 
        'token':token,
        'form':ResetPasswordForm()
        }
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.error(request, "Opps, The link has expired")
            return render(request, 'accounts/reset_email_form.html', {})
            
        
        messages.success(request, "verified")
        return render(request, 'accounts/reset_password.html', context)
    except DjangoUnicodeDecodeError as identifier:
        messages.error(request, "oops! something went wrong")
        return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/reset_password.html', context)

def register(request):
    return render (request, 'accounts/welcome.html')

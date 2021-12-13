from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from jobsapp.views import EditProfileView, EditEmployerProfileView
from .views import *

app_name = "accounts"

urlpatterns = [
    # path("employee/register/", RegisterEmployeeView, name="employee-registerr"),
    
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),
    
    path("employee/register/", RegisterJobSeeker.as_view(), name="employee-register"),
    
    path("employer/profile/update/", EditEmployerProfileView.as_view(), name="employer-profile-update"),
    
    path(
        "employee/profile/update/",
        EditProfileView.as_view(),
        name="employee-profile-update",
    ),
    path("welcome-register/", register, name="register-page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path('request-reset-email/', RequestResetEmail, name="request-reset-email"),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView, name='reset-password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


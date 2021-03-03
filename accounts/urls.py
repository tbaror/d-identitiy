from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('', auth_views.LoginView.as_view(), name = 'login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('changepass/', ChangeUserPassword.as_view(), name="changepass"),
    path("resetpass/", ResetRequestForm.as_view(), name="resetpass"),
    path("tokenchalenge/", .as_view(), name="")

    # path('signup/', SignUpView.as_view(), name='signup'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('changepass/', ChangeUserPassword.as_view(), name="changepass"),
    path("resetpass/", ResetRequestForm.as_view(), name="resetpass"),
    path("tokenchalenge/", TokenChalengeView.as_view(), name="tokenchalenge"),
    path("resetaction/", ResetActionView.as_view(), name="resetaction"),
    path("opsreset/", OperationStatusView.as_view(), name="opsreset"),
    path("opschange/", OpsChangeView.as_view(), name="opschange"),



    # path('signup/', SignUpView.as_view(), name='signup'),
]

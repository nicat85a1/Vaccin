from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path("verify-email/", views.email_verification_request, name="verify-email"),
    path("email/activate/<uidb64>/<token>/", views.email_verifier, name="email-activate")
]
from django.urls import path
from .import views


urlpatterns = [
    path('', views.index_page),
    path('userDash', views.user_dashboard),
    path('usersignup', views.user_sign_up),
    # path('login', views.login_user)
    path('token' , views.token_send , name="token_send"),
    path('verify/<auth_token>' , views.verify , name="verify"),
]
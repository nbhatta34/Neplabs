from django.conf import settings
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index_page),
    path('userDash', views.user_dashboard),
    path('usersignup', views.user_sign_up),
    path('logout', views.logout_user),
    path('token', views.token_send, name="token_send"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('documents', views.documents),
    path('addDocuments', views.add_documents),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="index/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="index/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="index/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="index/password_reset_done.html"), name="password_reset_complete"),
    path('distanceCalculator', views.vaccine_booking),
    path('distance_ajax', views.distance_ajax, name='distance_ajax'),
    path('vaccineBooking', views.distance_calculator, name='create_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from os import name
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
    path('addDocuments', views.add_documents, name='add_document'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="index/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="index/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="index/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="index/password_reset_done.html"), name="password_reset_complete"),
    path('distance_ajax', views.distance_ajax, name='distance_ajax'),
    path('delDocument',  views.delete_document, name='delete_document'),
    path('diagnostics', views.diagnostics, name='diagnostics'),
    path('profile', views.profile, name="profile"),
    path('editProfile', views.edit_profile, name="edit_profile"),
    path('upateImage', views.update_image, name="update_image"),
    path('laboratoryTest', views.laboratory_test),
    path('labResult', views.lab_result),
    path('addToCart', views.add_to_cart, name='add_to_cart'),
    path('deleteCartItem', views.delete_cart_item, name='delete_cart_item'),
    path('checkout', views.Checkout),
    path('esewa-request', views.esewa_request, name='esewa_request'),
    path('esewa-verify', views.esewa_verify),
    path('vaccine-booking', views.vaccine_booking, name="vaccine_booking"),
    path('delete-lab-result', views.delete_lab_result, name="delete_lab_result"),
    path('no_content', views.no_content)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





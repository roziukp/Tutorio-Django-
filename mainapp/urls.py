from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetCompleteView,PasswordChangeView,
                                       PasswordChangeDoneView)


urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('prof/', views.FillProfileData.as_view(), name='profile_registr'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.GetProfileData.as_view(), name='profile_data'),
    path('cvdata/', views.GetCVDAta.as_view(), name='cvdata'),
    path('profile/cvadd/', views.AddCV.as_view(), name='addcv'),
    path('posts/', views.get_posts_by_category, name='get_category'),
    url(r'^category/(?P<category_name>.+)/$', views.get_posts_by_category, name='post_by_category'),
    path('password-reset/', PasswordResetView.as_view(template_name='mainapp/password_reset_form.html'),
         name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='mainapp/password_reset-done.html'),
         name='password_reset_done'),
    url('^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(template_name='mainapp/password-reset-confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='mainapp/password-reset-complete.html'),
         name='password_reset_complete'),
    path('change-password/', PasswordChangeView.as_view(template_name='mainapp/change-password.html'),
         name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(template_name='mainapp/index.html'),
         name='password_change_done'),
    url(r'^post/(?P<post_id>.+)/$', views.get_one_post, name='onepost'),
    path('check/', views.check)
    # path('post/<int:post_id>/<int:parent_id>/', views.get_one_post, name='onepostcom'),
]


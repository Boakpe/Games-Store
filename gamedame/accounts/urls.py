from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', views.registerUserView, name = 'signup'),
    path('profile/', views.perfilView, name = 'perfil-view'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password')
]


""" urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) """
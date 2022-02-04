from django.urls import path
from django.views.generic import TemplateView

from .views import Signup, ProfileDetail


app_name = 'mainapp'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mainapp/base.html'), name='base'),
    path('clients/create/', Signup.as_view(), name='sign-up'),
    path('clients/<int:pk>/match/', ProfileDetail.as_view(), name='profile-detail'),
]

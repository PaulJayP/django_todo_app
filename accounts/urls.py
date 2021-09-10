from django.urls import path
from . import views
# from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
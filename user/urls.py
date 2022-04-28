from django.urls import path
from .views import CreateUserView, CreateTokenView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('login/', CreateTokenView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
]

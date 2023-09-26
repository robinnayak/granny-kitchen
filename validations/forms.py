from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']


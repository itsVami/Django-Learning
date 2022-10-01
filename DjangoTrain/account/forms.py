from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        user = kwargs.pop('user')

        super(ProfileForm , self).__init__(*args , **kwargs)

        self.fields['username'].help_text = None
        
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['Special_user'].disabled = True
            self.fields['Is_author'].disabled = True
        

    class Meta:
        model = User
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'Special_user' , 'Is_author'
        ]

        

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)    
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')      

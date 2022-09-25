from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(ProfileForm , self).__init__(*args , **kwargs)

        self.fields['username'].disabled = True
        self.fields['username'].help_text = None
        self.fields['email'].disabled = True
        self.fields['Special_user'].disabled = True
        self.fields['Is_author'].disabled = True

    class Meta:
        model = User
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'Special_user' , 'Is_author'
        ]

        
        

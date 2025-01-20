
from django import forms
from .models import CustomUser, Role, Department
from .models import Ticket, get_active_user



class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password', 'role', 'department']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    
    
class TicketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields = ['user', 'status', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use the get_active_user method to fetch only active users
        active_users = get_active_user()
        if active_users.exists():
            self.fields['user'].queryset = active_users
        else:
            self.fields['user'].queryset = self.fields['user'].queryset.none()
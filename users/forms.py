from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import CustomUser

# Form for creating a new user with Crispy Forms integration
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Fill your password..', 'autocomplete': 'new-password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password..', 'autocomplete': 'new-password'}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'role', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Fill your user name..', 'autocomplete': 'new-username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Fill your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Fill your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Fill your email address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print("Initializing CustomUserForm")  # <<< kontrola, jestli se form opravdu inicializuje
        
        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # jen jednoduché submit tlačítko pro test
        self.helper.add_input(Submit('submit', 'Create User'))
        print("CustomUserForm initialized")
        
        
        self.helper.form_class = 'row g-3'  # Bootstrap classes for spacing
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('role', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('password', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            # Submit('submit', 'Create User', css_class='btn btn-primary mt-3')
        )

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == "admin":
            from .models import CustomUser
            if CustomUser.objects.filter(role="admin").count() >= 4:
                raise forms.ValidationError("Maximum number of admins (4) has been reached.")
        return role

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user   



class CrispyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'new-username', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='mb-3 col-md-6'),
                Column('password', css_class='mb-3 col-md-6'),
            ),
        )




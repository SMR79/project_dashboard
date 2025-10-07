from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


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
        
        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
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
            Submit('submit', 'Create User', css_class='btn btn-primary mt-3')
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


# Form for editing user details (excluding password)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "role", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        # vyjmu custom parametry
        current_user = kwargs.pop("current_user", None)        
        
        # zavolám init ModelForm
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
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
            Submit('submit', 'Update User', css_class='btn btn-primary mt-3'),    
            HTML(f'<a href="{reverse("user_detail", args=[self.instance.id])}" class="btn btn-secondary mt-3">Cancel</a>')        
        )

        # Disable role field if current user is not admin
        if not (current_user and getattr(current_user, "role", None) == "admin"):
            self.fields["role"].disabled = True


# Custom Authentication Form with Crispy Forms integration
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
            Submit('submit', 'Login', css_class='btn btn-primary mt-3')
        )




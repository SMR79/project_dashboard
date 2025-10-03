from django import forms
from .models import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.form_class = 'row g-3'  # Bootstrap classes for spacing
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('description', css_class='col-md-12'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Submit('submit', 'Create Project', css_class='btn btn-primary mt-3')
        )
from django import forms
from .models import Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'supervisor_person', 'assigned_person', 'due_date', 'attachment', 'status', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['description'].widget.attrs.update({'rows': 3})       
        
        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.form_class = 'row g-3'  # Bootstrap classes for spacing
        self.helper.layout = Layout(
            Row(
                Column('project', css_class='col-md-6'),
                Column('title', css_class='col-md-6'),
            ),
            Row(
                Column('supervisor_person', css_class='col-md-6'),
                Column('assigned_person', css_class='col-md-6'),
            ),
            Row(
                Column('description', css_class='col-md-8'),
                Column('status', css_class='col-md-4'),
            ),
            Row(
                Column('attachment', css_class='col-md-6'),
            ),
            Row(
                Column('due_date'),
                Column('priority'),
                
            ),
            Submit('submit', 'Create Task', css_class='btn btn-primary mt-3')
        )
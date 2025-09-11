from django.db import models

class Task(models.Model):
    
    COMPLETED_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()    
    completed = models.CharField(choices=COMPLETED_CHOICES, default='pending')

    def __str__(self):
        return self.title
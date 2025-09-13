from django.db import models
from django.utils import timezone
from django.conf import settings

class Project(models.Model):

    STATUS_CHOICES = [ 
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]    

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planned')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")

    def save(self, *args, **kwargs):
        # pokud je projekt dokončen a end_date není vyplněno
        if self.status == 'completed' and not self.end_date:
            self.end_date = timezone.now().date()
        super().save(*args, **kwargs)        

    def __str__(self):
        return self.name

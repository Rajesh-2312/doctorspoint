from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils.timezone import now 
import logging
#CustomUser= get_user_model()

logger=logging.getLogger(__name__)

def get_active_user():
    activity_threshold = now() - timedelta(minutes=30)

    active_users= CustomUser.objects.filter(is_active=True).filter(
        models.Q(last_login__gte=activity_threshold) | models.Q(last_activity__gte=activity_threshold
        )).distinct()
    logger.info(f"Active User:{active_users}")
    return active_users
    
class ActiveUserMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = now()
            request.user.save()
        response = self.get_response(request)
        return response 

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_description = models.TextField()
    
    def __str__(self):
        return self.department_name 
    
    
    
class Role(models.Model):
    role_name = models.CharField(max_length=100)
    role_description = models.TextField()

    def __str__(self):
        return self.role_name
    
    

class CustomUser(AbstractUser):
    role= models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True,db_constraint=False) 
    department= models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,db_constraint=False) 
    last_activity=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.username
    
    
    
class Ticket(models.Model):
    STATUS_CHOICES=[
        ('Open','Open'),
        ('In Progress','In Progress'),
        ('Closed','Closed'),
    ]
    
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=True,related_name='tickets',db_constraint=False)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES) 
    description=models.TextField(blank=True, null=True) 
    raised_at=models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return f" Ticket for {self.user.username if self.user else 'No user'} || Status: {self.status} || Raised at: {self.raised_at}"
            
    def clean(self):
        if self.user is None:
            raise ValidationError('User cannot be null')    
        super().clean() 

    '''for session in sessions:
        data = session.get_decoded()  # Decode session data
        user_id = data.get('_auth_user_id')  # Get the user ID from the session
        if user_id:
            user_ids.append(user_id)  # Append user ID to the list
    # Return active users by filtering based on the collected user IDs
    return CustomUser.objects.filter(id__in=user_ids) '''   
           
class AddNewEmployee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)   
    Role=models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)  
    Department=models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)   
    MailId=models.EmailField(max_length=100)
    address=models.TextField(max_length=100)
    phone=models.IntegerField()
    
    def __str__(self):
        return f"Employee_name: {self.user.username} ||  Role: {self.Role} ||  Department: {self.Department}"    
    
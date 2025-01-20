from django.contrib import admin
from django import forms
from .models import Ticket,get_active_user
from django.contrib import admin
from .models import Department, Role, CustomUser, AddNewEmployee
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
import logging



admin.site.register(Department)
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(AddNewEmployee)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user', 'status', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_user=get_active_user()
        
        if active_user.exists():
            self.fields['user'].queryset = active_user  
        else:
            self.fields['user'].queryset = CustomUser.objects.all()
        
'''logger=logging.getLogger(__name__)        


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form=TicketForm
    list_display=['user','status','raised_at']
    list_filter=['status','raised_at']
    search_fields=['user__username', 'description']  
    actions=['mark_as_completed','raise_again']
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user=request.user
            self.message_user(request, "A valid user must be assigned to the ticket.")
            return  # Stop saving the ticket
        if not CustomUser.objects.filter(id=obj.user_id).exists():
            self.message_user(request, "The assigned user does not exist.")
            return
        super().save_model(request, obj, form, change)

     
    def mark_as_completed(self, request, queryset):
        updated_count=queryset.update(status='Closed')
        self.message_user(request, f"{updated_count} tickets are marked as completed")    
        
        
        
    def raise_again(self, request, queryset):
        updated_count=queryset.update(status='Open')
        self.message_user(request, f"{updated_count} tickets are raised again")
'''


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketForm
    list_display = ['user', 'status', 'raised_at']
    list_filter = ['status', 'raised_at']
    search_fields = ['user__username', 'description']
    actions = ['mark_as_completed', 'raise_again']

    def save_model(self, request, obj, form, change):
        if not obj.user:
            self.message_user(request, "A valid user must be assigned to the ticket.")
            return  # Stop saving the ticket
        if not obj.user.is_active:
            self.message_user(request, "The assigned user is not active.")
            return
        super().save_model(request, obj, form, change)

    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status='Closed')
        self.message_user(request, f"{updated_count} tickets marked as completed.")

    def raise_again(self, request, queryset):
        updated_count = queryset.update(status='Open')
        self.message_user(request, f"{updated_count} tickets raised again.")
from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserRegistrationForm, PasswordResetForm
from django.contrib.auth.hashers import make_password   
from django import forms
from django.contrib.auth import authenticate, login
from .models import CustomUser, Ticket
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse


class loginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)  

def login_user(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                form.add_error(None,"invalid username or password")     
    
    
    else:
        form = loginForm()
    return render(request,'login.html',{'form':form})   


   
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            return render(request,'login.html')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request,'home.html')


def reset_password(request):
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = get_object_or_404(CustomUser,username=username)  
            user.set_password("admin@123")
            user.save()
            return render(request, 'reset_password_done.html',{'username':username})  
    else:
        form = PasswordResetForm()
    return render(request,'reset_password.html',{'form':form}) 

@login_required
def user_tickets(request):
    tickets=Ticket.objects.filter(user__username=request.user)    
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')  # Get the ticket id from the form
        try:
            ticket = Ticket.objects.get(id=ticket_id, user__username=request.user)  # Ensure it's the correct user's ticket
            ticket.status = 'Closed'  # Update the ticket status to 'Completed'
            ticket.save()  # Save the ticket to apply the change
            return redirect('user_tickets')  # Redirect to the same page to see the updated ticket
        except Ticket.DoesNotExist:
            return HttpResponse("Ticket not found or you're not authorized to update this ticket.", status=404)

    return render(request, 'user_tickets.html', {'tickets': tickets})
        
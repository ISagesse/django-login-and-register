from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    else:
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
                first_name = f_name,
                last_name = l_name,
                email = email,
                password = new_password
            )
        request.session['userid'] = user.id
        return redirect('/home')

def login(request):
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        logged_user = user_email[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("/home")
    
    return redirect("/")

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    
    context = {
        'user' : User.objects.get(id=request.session['userid'])
    }

    return render(request, 'home.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

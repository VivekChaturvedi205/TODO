from django.shortcuts import render, redirect
from .models import MyUser,todolist
from django.http import HttpResponse
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def home(request):
    todo=todolist.objects.filter(user=request.user).all()
    print(request.user.id)
    print(todo)
    return render(request, 'home.html', {'todo':todo})

def add_task(request):
    if request.method=='POST':
        title=request.POST.get('title')
        details=request.POST.get('details')

        if title and details is None:
            messages.success(request, 'Please write some tittle & details.')
            return redirect("/")
        if title and details is not None:
            todo=todolist.objects.create(user=request.user ,title=title,details=details)
            print(request.user)
            todo.save()
            return redirect("/")
    return redirect('/')

def edit_task(request,id):
    todo=todolist.objects.get(id=id)
    i={
        "title":todo.title,
        "details":todo.details,
        "id":todo.id
    }
    return render(request, 'edit.html',{"i":i})

def update_task(request,id):
        todo=todolist.objects.get(id=id)
        todo.title=request.POST.get('title')
        todo.details=request.POST.get('details')
        import datetime 
        update_at=datetime.datetime.now()
        todo.created_at=update_at
        todo.save()
        todo={
            'todo':todolist.objects.filter(user=request.user).all()
        }
        return redirect('/')



def delete_task(request,id):
    todo=todolist.objects.get(id=id)
    todo.delete()
    return redirect('/')

def register(request):
    return render(request, 'register.html')


def reg_process(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('Password')
        password2 = request.POST.get('Password2')
        print(email)
        print(password)
        print(password2)

        try:
            if request.POST['Password'] != request.POST['Password2']:
                messages.success(request, 'Both Password are Not Same.')
                return redirect('/register')

            if MyUser.objects.filter(email=email).first():
                messages.success(request, 'Email Already Register.')
                return redirect('/register')
            Token=str(uuid.uuid4())
            myuser_obj = MyUser.objects.create(email=email ,Token=Token)
            myuser_obj.set_password(password)
            myuser_obj.save()
            send_mail_registration(email,Token)
            return redirect('/success')

        except Exception as e:
            
            print(e)

    return redirect('/register')

def logout_view(request):
    auth.logout(request)
    return redirect('/')

def send_mail_registration(email, Token):
    subject = "Your accounts needs to Verifiy"
    message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{Token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

def verify_email(request,Token):
    try:
        myuser=MyUser.objects.filter(Token=Token).first()
        if myuser.email_verified:
            messages.success(request, 'Your Email is already verified.')
            return redirect('/login')

        if myuser:
            myuser.email_verified = True
            myuser.save()
            messages.success(request, 'Your Email is verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def log_process(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        if MyUser.objects.filter(email=email).first() is None:
            messages.success(request, 'Email not Found')
            return redirect("/login")
            
        if not MyUser.objects.filter(email=email).first().email_verified:
            messages.success(request, 'Please Check your mail and verified it')
            return redirect("/login")

        user=auth.authenticate(email=email, password=password)

        if user is None:
            messages.success(request, 'Password Incorrect')
            return redirect("/login")
        
        auth.login(request,user)
        
        return redirect('/')

def error(request):
    return render(request, 'error.html')

def login(request):
    return render(request, 'login.html')

def success(request):
    return render(request, 'success.html')

def token(request):
    return render(request, 'token.html')

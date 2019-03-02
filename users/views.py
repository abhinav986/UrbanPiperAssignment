from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
import simplejson as json
from django.http import HttpResponse
from django.contrib.auth.models import User
from test1.global_function import CustomValidations as GF
from .models import Role


# Create your views here.

def homePage(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request,'base.html')
        else:
            return render(request,'login.html')

@csrf_exempt
def custom_login(request):
    if 'username' not in request.POST:
        context = {"error": "Please enter username"}
        return render(request,'login.html',context)
    else:
        username = request.POST['username']
    if 'password' not in request.POST:
        context = {"error": "Please enter password"}
        return render(request,'login.html',context)
    else:
        password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        role = Role.objects.get(user=user)
        if role.role == 2:
            return redirect("/manager/dashboard/")
        elif role.role == 1:
            return redirect("/delivery-boy/dashboard/")
    else:
        context = {"error": "Username or Password is incorrect"}
        return render(request,'login.html',context)

def custom_logout(request):
    logout(request)
    return render(request,'login.html')



@csrf_exempt
def createUser(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'signup.html', context)

    if request.method == 'POST':
        #parameter validation
        string = []
        stringRequired = ['password1','password2','email','first_name','last_name','role']
        inte = []
        intRequired = []
        msg, status = GF.dataValidation(request, string, stringRequired, inte, intRequired)
        if status == 0:
            return HttpResponse(json.dumps({'status': 0, 'error': msg}))

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            pass
        else:
            context = { 'error': 'User Already Exist'}
            return render(request, 'signup.html', context)
        #password match check
        if password1 != password2:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Password Mismatch'}))

        try:
            user = User.objects.create_user(email, email , password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            role = Role()
            role.user = user
            role.role = request.POST['role']
            role.save()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))
        context = {'message': 'Sucessfully Created'}
        return render(request, 'login.html',context)

def api(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 1, 'mdg': 'Login'}))
        else:
            return HttpResponse(json.dumps({'status': 0, 'mdg': ' not Login'}))

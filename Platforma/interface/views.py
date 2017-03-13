from django.shortcuts import render
from django.http import HttpResponse
import django.contrib.auth
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from interface.models import Experiment 
# Create your views here.

# @login_required(login_url='/login')
def home(request):
	# vata iz baze podatke
	data = dict()
	data["content"] = dict()
	data["content"]["isLogin"] = request.user.is_authenticated

	return render(request, 'interface/home.html', data)

def login(request):
	if request.user.is_authenticated:
		return redirect('/');
		
	data = dict();
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
	
		user = authenticate(username=username, password=password)
		if user is not None:
			django.contrib.auth.login(request, user)
			return redirect('/');
		else:
			data["login_error"] = True
	
	return render(request, 'interface/login.html', data)

def register(request):
	if request.user.is_authenticated:
		return redirect('/');
	
	data = dict();
	
	if request.method == "POST":
                #username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password1']
                password2 = request.POST['password2']
                
                if User.objects.filter(username=username).exists():
                        data["register_error"] = True
                        data["name_error"] = True
                        data["error_message"] = "Postoji korisnik sa tavkim imenom"
                else:
                        if password == password2 and password != "":
                                User.objects.create_user(username, email, password)
                                user = authenticate(username=username, password=password)
                                django.contrib.auth.login(request, user)
                                return redirect('/');
                        else:
                                data["register_error"] = True
                        
	return render(request, 'interface/register.html', data)

# @login_required(login_url='/login')
def platform(request):
	# vata iz baze podatke
	data = dict()
	data["content"] = dict()
	data["content"]["isLogin"] = request.user.is_authenticated
	data["experiments"] = Experiment.objects.all().order_by("-datum_kreiranja")
	
	return render(request, 'interface/platform.html', data)

@login_required(login_url='/login')
def support(request):
	# vata iz baze podatke
	data = dict()
	data["content"] = dict()
	data["content"]["isLogin"] = request.user.is_authenticated
	
	return render(request, 'interface/support.html', data)

@login_required(login_url='/login')
def platform_page(request, experimentID):
	# vata iz baze podatke
	data = dict()
	data["content"] = dict()
	data["content"]["isLogin"] = request.user.is_authenticated
	data["content"]["experiment"] = Experiment.objects.get(pk=experimentID)
	
	return render(request, 'interface/platform_page.html', data)

@login_required(login_url='/login')
def logout(request):
	django.contrib.auth.logout(request)
	return redirect('/')

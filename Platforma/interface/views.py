from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import django.contrib.auth
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from interface.models import Experiment
from Utils import formatYTUrl

# service
import socket
import sys
from thread import *
import time
import json
from Packages.Package import Package
from Packages.PackageType import PackageType
from thread import *
import hashlib
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

	# filter video url (just yt support!!)
	data["content"]["experiment"].demo_video = formatYTUrl(data["content"]["experiment"].demo_video)

	# racuna pregled
	data["content"]["experiment"].broj_pregleda = data["content"]["experiment"].broj_pregleda + 1
	Experiment.objects.filter(pk=experimentID).update(broj_pregleda=data["content"]["experiment"].broj_pregleda)
	
	return render(request, 'interface/platform_page.html', data)

@login_required(login_url='/login')
def logout(request):
	django.contrib.auth.logout(request)
	return redirect('/')

# Zdravko - testing
@login_required(login_url='/login')
def service(request):
	if request.GET.get('eid') and request.GET.get('t'):
		experimentID = request.GET['eid'];
		requestType = request.GET['t']

		exp = None

		error = {"error": "unknown"}

		try:
			exp = Experiment.objects.get(pk=experimentID)
		except:
			error["error"] = "Unvalid experiment."
			return JsonResponse(error)

		API_KEY = exp.apikey

		HOST = ''

		ADDRESS = exp.adresa
		PORT = 1337

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		token_value = hashlib.sha224(str(time.time() * 1000)).hexdigest()

		data = None

		if requestType == "token":
			data = Package({'value':token_value, 'time':time.time()}, PackageType.Token) # startTime, period
		elif requestType == "info":
			if request.GET.get('token'):
				data = Package({'value':request.GET['token']}, PackageType.Info)
			else:
				data = Package({}, PackageType.Info)
		else:
			error["error"] = "Unvalid request type."
			return JsonResponse(error)

		try:
			s.bind((HOST, 0))
			s.connect((ADDRESS, PORT))

			#s.send(str.encode('Welcome, type your info\n'))
			s.sendall(data.getJSON())
			time.sleep(0.1)
			data = s.recv(1024)
			s.close();

			jsonData = json.loads(data)

			if requestType == "token":
				packOut = {"token_value": None}

				if "header" in jsonData and "message" in jsonData["header"] and jsonData["header"]["message"] == "successfully added":
					packOut["token_value"] = token_value

				return JsonResponse(packOut)

			return JsonResponse(jsonData)
		except socket.error as e:
			error["error"] = "Experiment in unaccessible."
		finally:
			s.close()

		#return HttpResponse("<p>" + exp.apikey+ " " + requestType + "</p>")

	return JsonResponse(error)
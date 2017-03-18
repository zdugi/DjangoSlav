from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import django.contrib.auth
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from interface.models import Experiment
from interface.Utils import formatYTUrl
from interface.models import PravaPristupa

from interface.models import Tokeni

# service
import socket
import sys
import time
import json
from Packages.Package import Package
from Packages.PackageType import PackageType
import hashlib
import datetime
from Crypto.Cipher import AES

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
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password1']
                password2 = request.POST['password2']
                
                if User.objects.filter(username=username).exists():
                        data["register_error"] = True
                        data["error_type"] = True
                        if User.objects.filter(email=email).exists():
                                data["error_message"] = "Postoji korisnik sa tavkim korisnickim imenom i email-om"
                        else:
                                data["error_message"] = "Postoji korisnik sa tavkim korisnickim imenom"
                else:
                        if password == password2 and password != "":
                                new_user = User.objects.create_user(username, email, password)
                                new_user.is_active = True
                                new_user.first_name = first_name
                                new_user.last_name = last_name
                                new_user.save()
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
	currentUser = request.user
	prava = PravaPristupa.objects.filter(user_id_id = currentUser.id).values('eksperiment_id')
	data["experiments"] = Experiment.objects.filter(id__in = prava).order_by("-datum_kreiranja")
	#data["experiments"] = Experiment.objects.all().order_by("-datum_kreiranja")
	data["experiments1"] = Experiment.objects.exclude(id__in = prava).order_by("-datum_kreiranja")
       
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
	data["content"]["haveAccess"] = False
	data["content"]["token"] = ""
	token = Tokeni.objects.filter(user_id=request.user, eksperiment_id=Experiment.objects.get(pk=experimentID), endVreme__gte=datetime.datetime.now()).values()
	if len(token) > 0:
		data["content"]["token"] = token[0]["token"]

	if len(PravaPristupa.objects.filter(user_id_id = request.user.id, eksperiment_id_id  = experimentID).values()) > 0:
		data["content"]["haveAccess"] = True
		
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
	error = {"error": "unknown"}

	if request.GET.get('eid') and request.GET.get('t'):
		experimentID = request.GET['eid'];
		requestType = request.GET['t']

		if len(PravaPristupa.objects.filter(user_id_id = request.user.id, eksperiment_id_id  = experimentID).values()) <= 0:
			return JsonResponse(error)

		exp = None

		try:
			exp = Experiment.objects.get(pk=experimentID)
		except:
			error["error"] = "Unvalid experiment."
			return JsonResponse(error)

		API_KEY = exp.apikey

		key = API_KEY[:32];
		iv = API_KEY[0:16];

		HOST = ''

		ADDRESS = exp.adresa
		PORT = 1337

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		token_value = hashlib.sha224(str(time.time() * 1000)).hexdigest()

		data = None

		if requestType == "token":
			# provera da li je vec uzeo token
			t = datetime.datetime.now()

			tokens = Tokeni.objects.filter(user_id=request.user, eksperiment_id=Experiment.objects.get(pk=experimentID), endVreme__gte=t)

			if len(tokens.values()) > 0:
				error["error"] = "Vec ste prijavljeni na eksperiment!"
				return JsonResponse(error)

			data = Package({'value':token_value, 'time':time.time()}, PackageType.Token) # startTime, period
		elif requestType == "info":
			# slanje direktno RPI
			if request.GET.get('token'):
				data = Package({'value':request.GET['token']}, PackageType.Info)
			else:
				data = Package({}, PackageType.Info)
			# || varijanta - provera u nasoj bazi?!
		else:
			error["error"] = "Unvalid request type."
			return JsonResponse(error)

		try:
			s.bind((HOST, 0))
			s.connect((ADDRESS, PORT))
			
			cipher = AES.new(key, AES.MODE_CFB, iv)
			s.sendall(cipher.encrypt(data.getJSON()))
			time.sleep(0.1)
			data = s.recv(1024)
			s.close();

			cipher = AES.new(key, AES.MODE_CFB, iv)
			jsonData = json.loads(cipher.decrypt(data))

			if requestType == "token":
				packOut = {"token_value": None}

				if "header" in jsonData and "message" in jsonData["header"] and jsonData["header"]["message"] == "successfully added":
					packOut["token_value"] = token_value
					delta = int(jsonData["value"]["exp"])
					# ubacuje token u bazu

					t = datetime.datetime.now()
					d = t + datetime.timedelta(0, delta)
					# mozda i radi?!
					dbToken = Tokeni(user_id=request.user, eksperiment_id=Experiment.objects.get(pk=experimentID), startVreme=t, endVreme=d, token=token_value)
					dbToken.save()

					return JsonResponse(packOut)

				return JsonResponse(jsonData)

			return JsonResponse(jsonData)
		except socket.error as e:
			error["error"] = "Experiment in unaccessible."
		finally:
			s.close()

		#return HttpResponse("<p>" + exp.apikey+ " " + requestType + "</p>")

	return JsonResponse(error)

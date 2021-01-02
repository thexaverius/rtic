from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie, Preference, Site
from .forms import PreferenceForm
from django.contrib import messages
from django.db import connection
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
import webbrowser

# Create your views here.
def test(request):
	webbrowser.open('http://www.nu.nl')
	webbrowser.open('http://www.ad.nl')
	webbrowser.open('http://www.telegraaf.nl')
	return redirect('home')

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('Je bent nu ingelogd.'))
			return redirect('home')

		else:
			messages.success(request, ('Fout opgetreden bij het inloggen.'))
			return redirect('login')
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('Je bent nu uitgelogd.'))
	return redirect('home')

def home_oud(request):
	if request.user.is_authenticated:
		user_id = request.user.id
		insert = insert_missing_user_preferences(user_id)
	
	else:
		#haal maar de voorkeuren van admin op en uiteraard niets inserten.
		user_id = 1
		insert = None
		messages.success(request, ('Login om je voorkeuren te beheren.'))

	activeCategories = Categorie.objects.filter(catActief=True)
	preferences = Preference.objects.filter(site__categorie__catActief=True).filter(site__sitActief=True).filter(user__id=user_id)
	preferenceJS = Preference.objects.filter(site__categorie__catActief=True).filter(site__sitActief=True).filter(preStart=True).filter(user__id=user_id)
	#myrow = test_sql('NU.nl')
	return render(request,'home.html',
		{
		'activeCategories': activeCategories, 
		'preferences': preferences,
		'preferenceJS': preferenceJS, 
		'insert': insert, 
		'user_id': user_id
		})

def home(request):
	if request.user.is_authenticated:
		user_id = request.user.id
		insert = insert_missing_user_preferences(user_id)
	
	else:
		#haal maar de voorkeuren van admin op en uiteraard niets inserten.
		user_id = 1
		insert = None
		messages.success(request, ('Login om je voorkeuren te beheren.'))

	activeCategories = Categorie.objects.filter(catActief=True)
	preferences = Preference.objects.filter(site__categorie__catActief=True).filter(site__sitActief=True).filter(user__id=user_id)
	preferenceJS = Preference.objects.filter(site__categorie__catActief=True).filter(site__sitActief=True).filter(preStart=True).filter(user__id=user_id)
	#myrow = test_sql('NU.nl')
	return render(request,'home2.html',
		{
		'activeCategories': activeCategories, 
		'preferences': preferences,
		'preferenceJS': preferenceJS, 
		'insert': insert, 
		'user_id': user_id
		})

def cross(request, list_id):
	if request.user.is_authenticated:
		#item = Preference.objects.get(pk=list_id)
		#item = get_object_or_404(Preference, pk=list_id)

		try:
			item = Preference.objects.get(pk=list_id)
		except ObjectDoesNotExist:
			messages.success(request, ('Dit item bestaat niet.'))
			return redirect('home')

		#extra controleren of dezelfde gebruiker is ingelogd, misschien gebruikt iemand de URL-hack
		if item.user.id == request.user.id: 
			item.preStart = True
			item.save()
			messages.success(request, (item.site.sitOmschrijving + ' is toegevoegd aan de quickstart.'))
		else:
			messages.success(request, ('Dit item kan door u niet bewerkt worden.'))

		return redirect('home')
	else:
		messages.success(request, ('Login om voorkeuren op te slaan.'))
		return redirect('home')

def uncross(request, list_id):
	if request.user.is_authenticated:
		#item = Preference.objects.get(pk=list_id)
		#item = get_object_or_404(Preference, pk=list_id)

		try:
			item = Preference.objects.get(pk=list_id)
		except ObjectDoesNotExist:
			messages.success(request, ('Dit item bestaat niet.'))
			return redirect('home')

		#extra controleren of dezelfde gebruiker is ingelogd, misschien gebruikt iemand de URL-hack
		if item.user.id == request.user.id: 
			item.preStart = False
			item.save()
			messages.success(request, (item.site.sitOmschrijving + ' is verwijderd uit de quickstart.'))
		else:
			messages.success(request, ('Dit item kan door u niet bewerkt worden.'))

		return redirect('home')
	else:
		messages.success(request, ('Login om voorkeuren op te slaan.'))
		return redirect('home')

def insert_missing_user_preferences(userid):	
	with connection.cursor() as cursor:
		sql = """
		SELECT %s, launcher_site.id
		FROM launcher_site
		LEFT JOIN launcher_preference ON launcher_preference.site_id = launcher_site.id
									  AND launcher_preference.user_id = %s
		WHERE launcher_preference.id IS NULL
		"""
		cursor.execute(sql,[userid, userid])
		rows = cursor.fetchall()

		sql2 = """
		INSERT INTO launcher_preference (user_id, site_id) 
		VALUES (%s,%s) 
		"""
		cursor.executemany(sql2, rows)
	
	return True

def test_sql(self):
	#qs = Preference.objects.filter(user__username='admin')
	qs = Preference.objects.all()
	return qs.query
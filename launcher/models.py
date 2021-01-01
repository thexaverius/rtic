from django.conf import settings
from django.db import models

# Create your models here.
class Categorie(models.Model):
	catOmschrijving = models.CharField(max_length=100)
	catActief = models.BooleanField(default=True)
	catVolgorde = models.IntegerField(default=0)

	class Meta:
		ordering = ['-catActief','catVolgorde','catOmschrijving']

	def __str__(self):
		if self.catActief:
			actief = 'actief'
		else:
			actief = 'inactief'
		return self.catOmschrijving + ' (' + actief + ')' + ' [' + str(self.catVolgorde) + ']'

class Site(models.Model):
	sitOmschrijving = models.CharField(max_length=100)
	sitUrl = models.CharField(max_length=100)
	categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT)
	sitActief = models.BooleanField(default=True)

	class Meta:
		ordering = ['-sitActief','categorie','sitOmschrijving']

	def __str__(self):
		if self.sitActief:
			actief = 'actief'
		else:
			actief = 'inactief'
		return self.sitOmschrijving + ' | ' + self.sitUrl + ' | ' + self.categorie.catOmschrijving + ' [' + str(self.categorie.catVolgorde)  + ']' + ' (' + actief + ')'

class Preference(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
	preStart = models.BooleanField(null=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'site'], name='unique_preference'),
		]

	def __str__(self):
		start = self.preStart
		if start == True:
			startApp = 'Starten'
		elif start == False:
			startApp = 'Niet Starten'
		else:
			startApp = '---'

		return self.user.username + ' | ' + self.site.sitOmschrijving + ' - ' + self.site.categorie.catOmschrijving + ' (' + startApp + ')'
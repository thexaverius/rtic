from django.contrib import admin
from .models import Categorie, Site, Preference
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class CategorieResource(resources.ModelResource):

    class Meta:
        model = Categorie

class CategorieAdmin(ImportExportActionModelAdmin):
    pass

class SiteResource(resources.ModelResource):

    class Meta:
        model = Categorie

class SiteAdmin(ImportExportActionModelAdmin):
    pass

class PreferenceResource(resources.ModelResource):

    class Meta:
        model = Categorie

class PreferenceAdmin(ImportExportActionModelAdmin):
    pass

# Register your models here.
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Preference, PreferenceAdmin)
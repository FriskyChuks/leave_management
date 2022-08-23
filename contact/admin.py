from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

@admin.register(Continent,Country,State,LocalGovernmentArea)
class ViewAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Contact)
# admin.site.register(State)
admin.site.register(Address)
# admin.site.register(Continent)
# admin.site.register(Country)
# admin.site.register(LocalGovernmentArea)
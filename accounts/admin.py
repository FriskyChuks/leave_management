from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    pass


# admin.site.register(User)
admin.site.register(Gender)
admin.site.register(SubUnit)
admin.site.register(Unit)
admin.site.register(Department)
admin.site.register(Directorate)
admin.site.register(UserGroup)


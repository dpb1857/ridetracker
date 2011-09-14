
from django.contrib import admin

from models import *


class ControlAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'distance')
    list_editable = ('name', 'distance')

admin.site.register(Control, ControlAdmin)

from models import *
from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)

class OutputAdmin(admin.ModelAdmin):
    pass
admin.site.register(Output, OutputAdmin)

from django.contrib import admin
from .models import LocationLevel, Location

class LocationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_code', 'parent')
    search_fields = ('name', 'location_code')
    list_filter = ('parent',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_level', 'parent')
    search_fields = ('name', 'location_level__name')
    list_filter = ('location_level', 'parent')

admin.site.register(LocationLevel, LocationLevelAdmin)
admin.site.register(Location, LocationAdmin)

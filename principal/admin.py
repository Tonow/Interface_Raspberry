from django.contrib import admin
from .models import TemperatureActuelle, TemperatureLac


class TemperatureAdmin(admin.ModelAdmin):
    list_display   = ('date_ajout', 'degres')
    list_filter    = ('date_ajout', 'degres',)
    date_hierarchy = 'date_ajout'
    ordering       = ('date_ajout', )
    search_fields  = ('date_ajout', 'degres')

# class GraphAdmin(admin.ModelAdmin):
#     list_display   = ('date_ajout', 'graph')
#     list_filter    = ('date_ajout', 'graph',)
#     date_hierarchy = 'date_ajout'
#     ordering       = ('date_ajout', )
#     search_fields  = ('date_ajout', 'graph')


admin.site.register(TemperatureActuelle, TemperatureAdmin)
admin.site.register(TemperatureLac, TemperatureAdmin)
# admin.site.register(Graphique, GraphAdmin)
# Register your models here.

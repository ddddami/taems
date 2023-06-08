from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import State, LGA, Address
# Register your models here.


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'lga', 'state')

    def state(self, address):
        return address.lga.state


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lgas')

    def lgas(self, state):
        url = (
            reverse('admin:location_lga_changelist')
            + '?'
            + urlencode({
                'state__id': str(state.id)
            }))

        return format_html('<a href="{}">{} LGAs</a>', url, state.lgas_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(lgas_count=Count('lga'))


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')

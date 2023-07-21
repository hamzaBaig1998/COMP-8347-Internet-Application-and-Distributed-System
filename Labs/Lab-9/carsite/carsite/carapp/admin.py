from django.contrib import admin
from carapp.models import CarType, Vehicle, Buyer, OrderVehicle, GroupMember
from django.contrib.auth.admin import UserAdmin


class BuyerAdmin(UserAdmin):
    ...


# Register your models here.
admin.site.register(CarType)
admin.site.register(Vehicle)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(OrderVehicle)
admin.site.register(GroupMember)

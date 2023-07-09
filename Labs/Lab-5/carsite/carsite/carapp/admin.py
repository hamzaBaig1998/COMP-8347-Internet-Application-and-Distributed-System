from django.contrib import admin
from carapp.models import CarType, Vehicle, Buyer, OrderVehicle, GroupMember

# Register your models here.
admin.site.register(CarType)
admin.site.register(Vehicle)
admin.site.register(Buyer)
admin.site.register(OrderVehicle)
admin.site.register(GroupMember)

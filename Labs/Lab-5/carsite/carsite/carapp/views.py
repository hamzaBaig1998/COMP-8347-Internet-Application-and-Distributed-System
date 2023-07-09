# # Import necessary classes
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
#
# from .models import Vehicle, GroupMember
#
#
# # Create your views here.
# def homepage(request):
#     cartype_list = Vehicle.objects.order_by('-car_price')[:10]
#     response = HttpResponse()
#     heading1 = '<p>' + 'Different Types of Cars:' + '</p>'
#     response.write(heading1)
#     for cartype in cartype_list:
#         para = '<p> Car Type = ' + str(cartype) + ' and price = ' + str(cartype.car_price) + '</p>'
#         response.write(para)
#     return response
#
#
# def aboutus(request):
#     para = '<p> This is a Car Showroom </p>'
#     response = HttpResponse()
#     response.write(para)
#     return response
#
# def cardetail(request, cartype_no):
#     cartype_list = Vehicle.objects.all()
#     response = HttpResponse()
#     heading1 = '<h1>' + 'Vehicles:' + '</h1>'
#     response.write(heading1)
#     found = False
#     for cartype in cartype_list:
#         if int(cartype.car_type.id) == int(cartype_no):
#             print(cartype)
#             para = '<p> Car Type = ' + str(cartype.car_type) + ' and name = ' + str(cartype) + '</p>'
#             response.write(para)
#             found = True
#
#     if found:
#         return response
#
#     response.write(get_object_or_404(Vehicle, car_type=cartype_no))
#     return response
#
#
# def lab_members(request):
#     members = GroupMember.objects.order_by('first_name')
#     context = {
#         'members': members
#     }
#     return render(request, 'lab_members.html', context)

# Differences between FBV and CBV
# 1. The syntax for both views is different, as one is function based and the other uses class definitions.
# 2. CBVs inherit from the View class and the FBVs don't have a base class
# 3. CBVs have methods such as get() and post(), we have only used get() in this lab.
# 4. Code organization is much better in classes, so CBVs have a much organized code, which doesn't seem like a big
# problem for this lab as the code isn't that long but as the code base increases in size, CBVs will prove to be easily
# readable.
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .forms import OrderVehicleForm
from .models import Vehicle, GroupMember, CarType, Buyer
from django.shortcuts import render


class HomepageView(View):
    def get(self, request):
        # cartype_list = Vehicle.objects.order_by('-car_price')[:10]
        # heading1 = '<p>' + 'Different Types of Cars:' + '</p>'
        # cartype_html = [f'<p> Car Type = {cartype} and price = {cartype.car_price}</p>' for cartype in cartype_list]
        # response_html = ''.join(cartype_html)
        # return HttpResponse(heading1 + response_html)
        cartype_list = CarType.objects.all().order_by('id')
        # Pass the cartype_list variable as context to the 'homepage.html' template
        return render(request, 'carapp/homepage.html', {'cartype_list': cartype_list})


class AboutUsView(View):
    def get(self, request):
        # para = '<p> This is a Car Showroom </p>'
        # return HttpResponse(para)
        # Not passing any context variable
        return render(request, 'carapp/aboutus.html')


class CarDetailView(View):
    def get(self, request, cartype_no):
        # cartype_list = Vehicle.objects.all()
        # heading1 = '<h1>' + 'Vehicles:' + '</h1>'
        # found = False
        # cartype_html = []
        # for cartype in cartype_list:
        #     if int(cartype.car_type.id) == int(cartype_no):
        #         print(cartype)
        #         para = f'<p> Car Type = {cartype.car_type} and name = {cartype}</p>'
        #         cartype_html.append(para)
        #         found = True
        #
        # if found:
        #     response_html = ''.join(cartype_html)
        #     return HttpResponse(heading1 + response_html)
        #
        # vehicle = get_object_or_404(Vehicle, car_type=cartype_no)
        # para = f'<p> Car Type = {vehicle.car_type} and name = {vehicle}</p>'
        # return HttpResponse(heading1 + para)
        car_type = get_object_or_404(CarType, id=cartype_no)
        vehicle_list = car_type.vehicles.all()
        # Passing car_type and vehicle_list as context variables to the template
        return render(request, 'carapp/cardetail.html', {'car_type': car_type, 'vehicle_list': vehicle_list})


class LabMembersView(View):
    def get(self, request):
        members = GroupMember.objects.order_by('first_name')
        context = {
            'members': members
        }
        return render(request, 'carapp/team.html', context)

class Vehicles(View):
    def get(self, request):
        cars = Vehicle.objects.filter(instock=True)
        return render(request, 'carapp/vehicles.html', {'cars': cars})

# class OrderHere(View):
#     def get(self, request):
#         return render(request, 'carapp/orderhere.html', {})


class SearchView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        return render(request, 'carapp/search.html', {'vehicles': vehicles})

    def post(self, request):
        vehicles = Vehicle.objects.all()
        selected_vehicle_id = request.POST.get('selected_vehicle')
        selected_vehicle = get_object_or_404(Vehicle, pk=selected_vehicle_id)
        return render(request, 'carapp/search.html', {'vehicles': vehicles,'selected_vehicle': selected_vehicle})

class OrderHereView(View):
    def get(self, request):
        msg = ''
        vehiclelist = Vehicle.objects.all()
        form = OrderVehicleForm()
        return render(request, 'carapp/orderhere.html', { 'form': form, 'msg': msg, 'vehiclelist': vehiclelist})

    def post(self, request):
        msg = ''
        vehiclelist = Vehicle.objects.all()
        form = OrderVehicleForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.quantity <= order.vehicle.inventory:
                order.vehicle.inventory -= order.quantity
                order.vehicle.save()
                order.status = 1
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fulfill your order.'
                return render(request, 'carapp/nosuccess_order.html', {'msg': msg})
        else:
            msg = 'There was an error with your order. Please try again.'

        return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})
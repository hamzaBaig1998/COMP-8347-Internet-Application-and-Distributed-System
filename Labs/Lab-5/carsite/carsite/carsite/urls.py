# from django.contrib import admin
# from django.urls import path, include
# from carapp import views
#
# urlpatterns = [path('', include('carapp.CarUrls')),
#                path('admin/', admin.site.urls),
#                path('members/', views.lab_members, name='lab_members')
#                ]

from django.urls import path, include
from django.contrib import admin
from carapp.views import HomepageView, AboutUsView, CarDetailView, LabMembersView, Vehicles, OrderHereView, SearchView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('car/<int:cartype_no>/', CarDetailView.as_view(), name='cardetail'),
    path('members/', LabMembersView.as_view(), name='lab_members'),
    path('vehicles/', Vehicles.as_view(), name='vehicles'),
    path('order/', OrderHereView.as_view(), name='order'),
    path('search/', SearchView.as_view(), name='search'),
    path('admin/', admin.site.urls),
]
# from django.urls import path
# from carapp import views
#
# app_name = 'carapp'
# urlpatterns = [
#     path('', views.homepage, name='homepage'),
#     path('carapp/aboutus', views.aboutus, name='aboutus'),
#     path('carapp/<cartype_no>', views.cardetail, name='cartype_no')
# ]

from django.urls import path
from .views import HomepageView, AboutUsView, CarDetailView, LabMembersView, Vehicles, OrderHereView, SearchView

app_name = 'carapp'
urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('car/<int:cartype_no>/', CarDetailView.as_view(), name='cardetail'),
    path('labmembers/', LabMembersView.as_view(), name='labmembers'),
    path('vehicles/', Vehicles, name='vehicles'),
    path('order/', OrderHereView.as_view(), name='order'),
    path('search/', SearchView.as_view(), name='search')
]
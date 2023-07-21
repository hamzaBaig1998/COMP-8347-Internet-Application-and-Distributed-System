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
from .views import HomepageView, AboutUsView, CarDetailView, LabMembersView, Vehicles, OrderHereView, SearchView, login_here, logout_here, list_of_orders

app_name = 'carapp'
urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('car/<int:cartype_no>/', CarDetailView.as_view(), name='cardetail'),
    path('labmembers/', LabMembersView.as_view(), name='labmembers'),
    path('vehicles/', Vehicles, name='vehicles'),
    path('order/', OrderHereView.as_view(), name='order'),
    path('search/', SearchView.as_view(), name='search'),
    path('login/', login_here, name='login_here'),
    path('logout/', logout_here, name='logout_here'),
    path('list_of_orders/', list_of_orders, name='list_of_orders'),
]
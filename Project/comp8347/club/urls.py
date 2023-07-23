from django.urls import path

from club.views import ClubView, PayView

app_name = 'club'

urlpatterns = [
    path('club/', ClubView.as_view(), name='club_details'),
    path('pay/', PayView.as_view(), name='pay'),
]

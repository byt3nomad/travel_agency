from django.urls import path
from api_travel_agency.views import HolidayView, HolidaySupportView, LocaitonView, LocationSupportView, ReservationView, ReservationSupportView



urlpatterns = [
    path('holidays/', HolidayView.as_view()),
    path('holiday/get_by_id/', HolidaySupportView.as_view()),
    path('locations/', LocaitonView.as_view()),
    path('location/get_by_id/', LocationSupportView.as_view()),
    path('reservations/', ReservationView.as_view()),
    path('reservation/get_by_id/', ReservationSupportView.as_view()),
]
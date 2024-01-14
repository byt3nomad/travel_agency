from .models import Holiday, Location, Reservation
from .serializers import HolidaySerializer, LocationSerializer, ReservationSerializer
from django.core import serializers


def create_reservation(request):
    data = extract_reservation_data(request)

    try:
        holiday_obj = Holiday.objects.get(auto_increment_id=data['holiday_id'])
        location_obj = Location.objects.get(auto_increment_id=data['location_id'])
        reservation = Reservation(
            contact_name=data['contact_name'],
            phone_number=data['phone_number'],
            holiday=holiday_obj,
            location=location_obj
        )
        reservation.save()
        return {'Success': 'Reservation created '}
    except Holiday.DoesNotExist:
        return {'Error': 'Holiday not found with the provided id.'}
    except Location.DoesNotExist:
        return {'Error': 'Location not found with the provided id.'}
    except Exception as e:
        return {'Error': f'Something went wrong: {str(e)}'}


def extract_reservation_data(request):
    return {
        'contact_name': request.data.get('contact_name'),
        'phone_number': request.data.get('phone_number'),
        'holiday_id': request.data.get('holiday_id'),
        'location_id': request.data.get('location_id')
    }

    
def delete_reservation(request):
    reserve_id = request.data.get('reservation_id')
    try:
        reseve_obj = Reservation.objects.get(auto_increment_id=reserve_id)
        reseve_obj.delete()
        return {'Success': 'deleted'}
    except Exception:
        return {'Error': 'Could not find reservation with that id!'}
    
    
def get_all_reservations(request):
    reservations = Reservation.objects.all()
    serialized = ReservationSerializer(reservations, many=True)
    return serialized


def get_reservation_by_id(request):
    reserve_id = request.data.get('reservation_id')
    try:
        reserve_obj = Reservation.objects.get(auto_increment_id=reserve_id)
        serialized = ReservationSerializer(reserve_obj)
        return serialized
    except Exception:
        return {'Error': 'There is no existing reservation with this id!'}

def edit_reservation(request):
    data = extract_reservation_data_for_edit(request)

    try:
        reservation = Reservation.objects.get(auto_increment_id=data['reserve_id'])
        updated_reservation = update_reservation_object(reservation, data)
        if isinstance(updated_reservation, dict) and 'Error' in updated_reservation:
            return updated_reservation  # Return error message if related objects are not found
        return ReservationSerializer(updated_reservation).data
    except Reservation.DoesNotExist:
        return {'Error': 'Reservation not found with the provided id.'}
    except Exception as e:
        return {'Error': str(e)}

     
def update_reservation_object(reservation, data):
    for field in ['contact_name', 'phone_number']:
        if data.get(field) is not None:
            setattr(reservation, field, data[field])

    if data.get('holiday_id'):
        try:
            holiday_obj = Holiday.objects.get(auto_increment_id=data['holiday_id'])
            reservation.holiday = holiday_obj
        except Holiday.DoesNotExist:
            return {'Error': 'There is no holiday with this id!'}

    if data.get('location_id'):
        try:
            location_obj = Location.objects.get(auto_increment_id=data['location_id'])
            reservation.location = location_obj
        except Location.DoesNotExist:
            return {'Error': 'There is no location with this id!'}

    reservation.save()
    return reservation
     

def extract_reservation_data_for_edit(request):
    return {
        'reserve_id': request.data.get('reservation_id'),
        'contact_name': request.data.get('contact_name'),
        'phone_number': request.data.get('phone_number'),
        'holiday_id': request.data.get('holiday_id'),
        'location_id': request.data.get('location_id')
    }

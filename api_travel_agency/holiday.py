from .models import Holiday, Location, Reservation
from .serializers import HolidaySerializer, LocationSerializer, ReservationSerializer
from django.core import serializers

def create_holiday(request):
    data = extract_holiday_data(request)
    
    try:
        location_obj = Location.objects.get(auto_increment_id=data['auto_inc_id'])
        holiday = Holiday(
            location=location_obj,
            title=data['title'],
            start_date=data['start_date'], 
            duration=data['duration'],
            price=data['price'],
            free_slots=data['free_slots'],
        )
        holiday.save()
        return {'Success': 'Holiday was created!'}
    except Exception:
        return {'Error:': 'Something went wrong while creating the holiday!'}
        
def extract_holiday_data(request):
    return {
        'title': request.data.get('title'),
        'start_date': request.data.get('start_date'),
        'duration': request.data.get('duration'),
        'price': request.data.get('price'),
        'free_slots': request.data.get('free_slots'),
        'auto_inc_id': request.data.get('id')
    }



def delete_holiday(request):
    holiday_id = request.data.get('id')
    
    try:
        holiday = Holiday.objects.get(auto_increment_id=holiday_id)
        holiday.delete()
        return True
    except Exception:
        return False
    

def get_all_holidays(request):
    
    holidays = Holiday.objects.all()
    serialized = HolidaySerializer(holidays, many=True)
    return serialized


def get_holiday_by_id(request):
    holiday_id = request.data.get('id')
    
    try:
        holiday = Holiday.objects.get(auto_increment_id=holiday_id)
        return HolidaySerializer(holiday, many=False)
    except Exception:
        return 'Error occured'
    
def edit_holiday(request):
    data = extract_holiday_data(request)
    data['location_id'] = request.data.get('location')
    holiday_id = request.data.get('id')

    try:
        obj = Holiday.objects.get(auto_increment_id=holiday_id)
        updated_holiday = update_holiday_object(obj, data)
        if isinstance(updated_holiday, dict) and 'Error' in updated_holiday:
            return updated_holiday  # Return error message if location is not found
        return HolidaySerializer(updated_holiday).data
    except Holiday.DoesNotExist:
        return {'Error': 'There is no holiday with this id!'}
    except Exception as e:
        return {'Error': str(e)}

def update_holiday_object(holiday, data):
    if data.get('location_id'):
        try:
            new_location = Location.objects.get(auto_increment_id=data['location_id'])
            holiday.location = new_location
        except Location.DoesNotExist:
            return {'Error': 'There is no location with this id!'}
    for field in ['title', 'start_date', 'duration', 'price', 'free_slots']:
        if data.get(field) is not None:
            setattr(holiday, field, data[field])
    holiday.save()
    return holiday


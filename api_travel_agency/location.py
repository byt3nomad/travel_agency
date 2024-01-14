from .models import Holiday, Location, Reservation
from .serializers import HolidaySerializer, LocationSerializer, ReservationSerializer
from django.core import serializers

def create_location(request):
    data = extract_location_data(request)

    try:
        location = Location(**data)
        location.save()
        return {'Success': 'Location was created!'}
    except Exception as e:
        return {'Error': f'Something went wrong: {str(e)}'}


def extract_location_data(request):
    return {
        'number': request.data.get('number'),
        'country': request.data.get('country'),
        'city': request.data.get('city'),
        'image_url': request.data.get('image_url'),
    }


def delete_location(request):
    location_id = request.data.get('id')
    
    try:
        location = Location.objects.get(auto_increment_id=location_id)
        location.delete()
        return True
    except Exception:
        return False
    

def get_all_locations(request):
    
    locations = Location.objects.all()
    serialized = LocationSerializer(locations, many=True)
    return serialized


def get_location_by_id(request):
    location_id = request.data.get('id')
    
    try:
        location = Location.objects.get(auto_increment_id=location_id)
        return LocationSerializer(location)
    except Exception:
        return {'Error': f'The location with the following id {location_id} does not exist!'}
    
def extract_location_data_for_edit(request):
    return {
        'number': request.data.get('number'),
        'country': request.data.get('country'),
        'city': request.data.get('city'),
        'image_url': request.data.get('image_url'),
        'loc_id': request.data.get('id_loc')
    }

def edit_location(request):
    data = extract_location_data_for_edit(request)

    try:
        location = Location.objects.get(auto_increment_id=data['loc_id'])
        updated_location = update_location_object(location, data)
        return LocationSerializer(updated_location).data
    except Location.DoesNotExist:
        return {'Error': 'Location not found with the provided id.'}
    except Exception as e:
        return {'Error': str(e)}


def update_location_object(location, data):
    for field in ['number', 'country', 'city', 'image_url']:
        if data.get(field) is not None:
            setattr(location, field, data[field])
    location.save()
    return location



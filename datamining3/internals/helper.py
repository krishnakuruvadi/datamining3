from .models import ZipCode, Attraction


'''
    {
      'business_status': 'OPERATIONAL',
      'geometry': {
        'location': {
          'lat': 37.30626470000001,
          'lng': -121.802796
        },
        'viewport': {
          'northeast': {
            'lat': 37.30755647989272,
            'lng': -121.8017538201073
          },
          'southwest': {
            'lat': 37.30485682010728,
            'lng': -121.8044534798927
          }
        }
      },
      'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/park-71.png',
      'icon_background_color': '#4DB546',
      'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/tree_pinlet',
      'name': 'Brigadoon Park',
      'opening_hours': {
        'open_now': True
      },
      'photos': [
        {
          'height': 900,
          'html_attributions': [
            '<a href="https://maps.google.com/maps/contrib/113368425708781781285">A Google User</a>'
          ],
          'photo_reference': 'AUacShglKucuvKFx1u-ewzi1tByVXfob7X6hPw5JZVxcVO5NyVcROtz4boTMYZVBKZPAdsuQXhP-VVhaTaTFuN3VWvVls-Y7WLSCyzz5LOLKPBi1XfQv244fbtS33JzlcFMKhF4vSgi6JhBgaFKFNjStRFdRK-jWz7Z4DHF9LWi6zyBXFPsK',
          'width': 1200
        }
      ],
      'place_id': 'ChIJsVvXRYItjoAR-UoZLZ2-VoA',
      'plus_code': {
        'compound_code': '854W+GV San Jose, California',
        'global_code': '849W854W+GV'
      },
      'rating': 4.4,
      'reference': 'ChIJsVvXRYItjoAR-UoZLZ2-VoA',
      'scope': 'GOOGLE',
      'types': [
        'park',
        'tourist_attraction',
        'point_of_interest',
        'establishment'
      ],
      'user_ratings_total': 437,
      'vicinity': 'Brigadoon Way, San Jose'
    }
    '''
def add_or_update_attractions(results, zip_code_obj):
    print(f'inside add_or_update_attractions')
    for result in results:
        try:
            add_or_update_attraction(result, zip_code_obj)
        except Exception as ex:
            print(f'failed to add attraction {ex}')

def add_or_update_attraction(result, zip_code_obj):
    print(f'inside add_or_update_attraction {result}')
    try:
        place_id = result['place_id']
        attraction = Attraction.objects.get(zip_code=zip_code_obj, place_id=place_id)
        if 'photos' in result and len(result['photos']) > 0:
            attraction.photo_reference = result['photos'][0]['photo_reference']
            attraction.save()
        print(f'attraction exists')
        #TODO: update the attraction info
    except Attraction.DoesNotExist:
        if result['business_status'].lower() == 'operational':
            print(f'adding attraction with info {result}')
            try:
                photo_reference = ""
                if 'photos' in result and len(result['photos']) > 0:
                    photo_reference = result['photos'][0]['photo_reference']
                a = Attraction.objects.create(
                    place_id = place_id,
                    latitude = result['geometry']['location']['lat'],
                    longitude = result['geometry']['location']['lng'],
                    data=result,
                    is_park = 'park' in result['types'],
                    is_tourist_attraction = 'tourist_attraction' in result['types'],
                    is_point_of_interest =  'point_of_interest' in result['types'],
                    is_establishment =  'establishment' in result['types'],
                    rating = result['rating'],
                    number_of_ratings = result['user_ratings_total'],
                    name = result['name'],
                    vicinity = result['vicinity'],
                    zip_code=zip_code_obj,
                    photo_reference=photo_reference
                )
            except Exception as ex:
                print(f'failed to add attraction {ex}')
        else:
            print(f'ignoring non operational attraction {result}')


def get_attractions(country, zip_code):
    try:
        if zip_code == '*':
            zip_objs = ZipCode.objects.filter(country=country)
            attractions = Attraction.objects.filter(zip_code__in=zip_objs)
            return attractions
        zip_obj = ZipCode.objects.get(country=country, zip_code=zip_code)
        attractions = Attraction.objects.filter(zip_code=zip_obj)
        return attractions
    except ZipCode.DoesNotExist:
        print(f'zip code not being tracked {zip_code}')
    return list()
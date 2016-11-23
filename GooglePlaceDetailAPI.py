import json
import requests
import csv
import os
import time
from collections import Counter

i = 5
key = ['AIzaSyDagLQyFaxkonqlXrYs6ATE52OTFqR8tl8', 
		'AIzaSyAzM507T0fwWT53MrlODoVzHErC7NLJ5LA',
		'AIzaSyBTRhdywFUJs19Z_vBTpluXLG97QzJ-ye4',
		'AIzaSyALmFOn9o_38v0_uOReo13AaTsnAuzgM2o',
		'AIzaSyDZM55nZ4utQcPFo3GA28nwjGQjTVSBlrc',
		'AIzaSyDvFS8JxXQ6q0bPePOTzcIvFeXT_dC5Lc8',
		'AIzaSyAQQVlUq0o6ydi2voL4ychdflpmpinsq74',
		'AIzaSyAx9aKulX6S01KZo6l7eUIKCIzjJKCoPys',
		'AIzaSyCSxFDPIv_Cs7qvmvHzD-C-BDfHq8U5hTk',
		'AIzaSyBk3HbKqzzzz7WFHqBjwLhdeKF-NIyt9yg',
		'AIzaSyCrUWdPyEWp5POErlre7pYOowZV4t2u-iM',
		'AIzaSyAGiYM4AZ-shzgozzyk_vTJzTVuIxkPiYA',
		'AIzaSyCx6gqmKc87ca7qtguMoSqcjetq3JeR-YI',
		'AIzaSyCcU_ID4YZ4maMxI3RD8N7wye1fDqE89xU',
		'AIzaSyDdli4REqafoLBv6bDChQAz7Z71nJ2xpiY',
		'AIzaSyDIlZodoajMC4jHr26JJEtLqH3YCTbVZIU',
		'AIzaSyCLJeI5HZMgW1GhZEC7vNgLQpKVumvlNsE']

key = 'AIzaSyB-aOVFpohnFJP_IPdNznth-3B7Mvih3b4'


def check_valid_response(ref_request):
	results = json.loads(ref_request.encode(('utf-8')))
	if results['status'] == 'ZERO_RESULTS':
		return False
	else:
		return True


def get_reference_id(formatted_places):
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&key={1}".format(formatted_places, key)
	
	ref_request = requests.get(url).text

	if check_valid_response(ref_request):
		results 	  	= json.loads(ref_request.encode(('utf-8')))
		return results
	else:
		return {'status': False}


def get_location_details(place_details):
	if place_details:
			geoLatitude 	= place_details['results'][0]['geometry']['location']['lat']
			geoLongitude	= place_details['results'][0]['geometry']['location']['lng']
			address=place_details['results'][0]['formatted_address']
			return(geoLatitude,geoLongitude,address)


def location_std(formatted_places):
	formatted_places = formatted_places
	reference = get_reference_id(formatted_places)
	print reference
	if reference['status']:
		place_details = get_reference_id(formatted_places)
		return (get_location_details(place_details))
	else:
		return(0,0,"notfound")


def start123(location):
    geoLatitude=0
    geoLongitude=0
    address=''
    try:
         [geoLatitude,geoLongitude,address]=location_std(location)
    except:
         print "error"
    # print type(address)
    address = address.encode('ascii','ignore')
    print type(address)
    print geoLatitude,geoLongitude,address
    return geoLatitude,geoLongitude,address


#start123("Churchgate")
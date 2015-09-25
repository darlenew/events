#!/usr/bin/env python
"""
customers.py

Let's say we have some customer records in a text file (customers.txt,
see below) -- one customer per line, JSON-encoded. We want to invite
any customer within 100km of our Dublin office (GPS coordinates
53.3381985, -6.2592576) for some food and drinks on us. 

Write a program that will read the full list of customers and output
the names and user ids of matching customers (within 100 km), sorted
by user id (ascending). 

You can use the first formula from this Wikipedia article to calculate
distance: https://en.wikipedia.org/wiki/Great-circle_distance but
don't forget to convert degrees to radians. Your program should be
tested.
"""
from math import pi, atan2, cos, sin, pow, sqrt, radians
from collections import namedtuple
import json

MEAN_EARTH_RADIUS = 6371 # km
INVITATION_RADIUS = 100 # km

class Point(object):
    def __init__(self, lat, long):
        self.lat = float(lat)
        self.long = float(long)

class Customer(object):
    def __init__(self, user_id, name=None, point=None):
        self.user_id = user_id
        self.name = name
        self.point = point

def distance(point1, point2, radius=MEAN_EARTH_RADIUS):
    """Return the distance, in kilometers, between points 1 and 2."""
    phi1, lambda1 = radians(point1.lat), radians(point1.long)
    phi2, lambda2 = radians(point2.lat), radians(point2.long)
    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1
    
    # based on Vincenty formula
    left = pow(cos(phi2) * sin(delta_lambda), 2) 
    right = pow(cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(delta_lambda), 2)
    numerator = sqrt(left + right)
    denominator = sin(phi1) * sin(phi2) + cos(phi1) * cos(phi2) * cos(delta_lambda)
    central_angle = atan2(numerator, denominator)
    
    return radius * central_angle
    
def load_json(path):
    """Load JSON data from a file and return list of Customer objects."""
    customers = []
    try:
        with open(path, 'r') as fd:
            data = fd.read()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return []
    except:
        raise

    for line in data.strip().split('\n'):
        d = json.loads(line)
        point = Point(d['latitude'], d['longitude']) # TODO validate data
        customer = Customer(d['user_id'], name=d['name'], point=point)  
        customers.append(customer)

    return customers

def invited(customers, origin, within=100):
    """Return a sorted list of customers to invite.

    Given a list of customer objects, return a sorted list of the ones
    within a certain distance, in kilometers, from the origin point.
    """
    nearby = [c for c in customers if distance(origin, c.point) < within]
    return sorted(nearby, key=lambda x: x.user_id)

if __name__ == "__main__":
    dublin_office = Point(53.3381985, -6.2592576)
    json_path = "customers.txt"

    customers = load_json(json_path)
    invited_customers = invited(customers, dublin_office)
    for c in invited_customers:
        print c.user_id, c.name
        

    

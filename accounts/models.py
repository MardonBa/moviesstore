from django.db import models
LOCATIONS = [
    {"city": "Atlanta", "state": "GA", "latitude": 33.7490, "longitude": -84.3880},
    {"city": "Boston", "state": "MA", "latitude": 42.3601, "longitude": -71.0589},
    {"city": "New York", "state": "NY", "latitude": 40.7128, "longitude": -74.0060},
    {"city": "Los Angeles", "state": "CA", "latitude": 34.0522, "longitude": -118.2437},
    {"city": "Chicago", "state": "IL", "latitude": 41.8781, "longitude": -87.6298},
    {"city": "Houston", "state": "TX", "latitude": 29.7604, "longitude": -95.3698},
    {"city": "Phoenix", "state": "AZ", "latitude": 33.4484, "longitude": -112.0740},
    {"city": "Philadelphia", "state": "PA", "latitude": 39.9526, "longitude": -75.1652},
    {"city": "San Antonio", "state": "TX", "latitude": 29.4241, "longitude": -98.4936},
    {"city": "San Diego", "state": "CA", "latitude": 32.7157, "longitude": -117.1611},
    {"city": "Dallas", "state": "TX", "latitude": 32.7767, "longitude": -96.7970},
    {"city": "San Jose", "state": "CA", "latitude": 37.3382, "longitude": -121.8863},
    {"city": "Austin", "state": "TX", "latitude": 30.2672, "longitude": -97.7431},
    {"city": "Jacksonville", "state": "FL", "latitude": 30.3322, "longitude": -81.6557},
    {"city": "Fort Worth", "state": "TX", "latitude": 32.7555, "longitude": -97.3308},
    {"city": "Columbus", "state": "OH", "latitude": 39.9612, "longitude": -82.9988},
    {"city": "Charlotte", "state": "NC", "latitude": 35.2271, "longitude": -80.8431},
    {"city": "San Francisco", "state": "CA", "latitude": 37.7749, "longitude": -122.4194},
    {"city": "Indianapolis", "state": "IN", "latitude": 39.7684, "longitude": -86.1581},
    {"city": "Seattle", "state": "WA", "latitude": 47.6062, "longitude": -122.3321},
    {"city": "Denver", "state": "CO", "latitude": 39.7392, "longitude": -104.9903},
    {"city": "Washington", "state": "DC", "latitude": 38.9072, "longitude": -77.0369},
]

LOCATION_CHOICES = [(loc["city"], f'{loc["city"]}, {loc["state"]}') for loc in LOCATIONS]
COORDS = {loc["city"]: (loc["latitude"], loc["longitude"]) for loc in LOCATIONS}

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Atlanta')
    location_chosen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.location})"
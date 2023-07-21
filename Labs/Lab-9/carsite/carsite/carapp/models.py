from django.db import models
from django.contrib.auth.models import User


class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    car_price = models.DecimalField(max_digits=10, decimal_places=6)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)

    # New field for car features
    CRUISE_CONTROL = 'CC'
    AUDIO_INTERFACE = 'AI'
    AIRBAGS = 'AB'
    AIR_CONDITIONING = 'AC'
    SEAT_HEATING = 'SH'
    PARK_ASSIST = 'PA'
    POWER_STEERING = 'PS'
    REVERSING_CAMERA = 'RC'
    AUTO_START_STOP = 'AS'

    FEATURE_CHOICES = (
        (CRUISE_CONTROL, 'Cruise Control'),
        (AUDIO_INTERFACE, 'Audio Interface'),
        (AIRBAGS, 'Airbags'),
        (AIR_CONDITIONING, 'Air Conditioning'),
        (SEAT_HEATING, 'Seat Heating'),
        (PARK_ASSIST, 'Park Assist'),
        (POWER_STEERING, 'Power Steering'),
        (REVERSING_CAMERA, 'Reversing Camera'),
        (AUTO_START_STOP, 'Auto Start/Stop'),
    )

    features = models.CharField(max_length=2, choices=FEATURE_CHOICES, blank=True)

    def __str__(self):
        return self.car_name


class Buyer(User):
    AREA_CHOICES = [
        ('W', 'Windsor'),
        ('LS', 'LaSalle'),
        ('A', 'Amherstburg'),
        ('L', 'Lakeshore'),
        ('LE', 'Leamington'),
        ('C', 'Chatham'),
        ('T', 'Toronto'),
        ('WL', 'Waterloo')]

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='C')
    interested_in = models.ManyToManyField(CarType)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class OrderVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.IntegerField(choices=[(0, 'cancelled'), (1, 'placed'), (2, 'shipped'), (3, 'delivered')])
    updated_at = models.DateField(auto_now=True)

    def total_price(self):
        return self.vehicle.car_price * self.quantity

    def __str__(self):
        return f"{self.quantity} X {self.vehicle.car_name}"


class GroupMember(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    semester = models.IntegerField()
    link = models.URLField(max_length=200)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

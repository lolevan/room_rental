from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='rooms/')
    capacity = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Add fields for additional images
    image_1 = models.ImageField(upload_to='rooms/', blank=True)
    image_2 = models.ImageField(upload_to='rooms/', blank=True)
    image_3 = models.ImageField(upload_to='rooms/', blank=True)
    image_4 = models.ImageField(upload_to='rooms/', blank=True)
    image_5 = models.ImageField(upload_to='rooms/', blank=True)
    image_6 = models.ImageField(upload_to='rooms/', blank=True)
    image_7 = models.ImageField(upload_to='rooms/', blank=True)
    image_8 = models.ImageField(upload_to='rooms/', blank=True)
    image_9 = models.ImageField(upload_to='rooms/', blank=True)
    image_10 = models.ImageField(upload_to='rooms/', blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    event_name = models.CharField(max_length=200, blank=True)  # Add event_name field
    advertise = models.BooleanField(default=False)  # Add advertise field

    def __str__(self):
        return f'{self.room.name} on {self.date} from {self.start_time} to {self.end_time}'


class Advertisement(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.PositiveIntegerField(default=1000)
    image = models.ImageField(upload_to='advertisements/')

    def __str__(self):
        return self.title

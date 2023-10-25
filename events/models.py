from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
# Create your models here.
class User(AbstractUser):
    wishlist = models.ManyToManyField("Events", blank=True, related_name="wishlists")
    image = models.ImageField(upload_to='users', default='events/users/default.jpg')
    mobile=models.CharField(max_length=10,blank=True)
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "image": self.image.url,
            "mobile": self.mobile,
            "email": self.email,
        }

class Events(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images',default='media/default.jpg',blank=True)
    club=models.CharField(max_length=64)
    ticket_price=models.DecimalField(max_digits=6,decimal_places=2)
    category=models.CharField(max_length=64,default='general')
    duration = models.DurationField(default=timedelta(hours=3))
    tickets=models.IntegerField(default=100)

    def __str__(self):
        return f"{self.title} - {self.date} - {self.location} - {self.image} "
    
    def date_formatted(self):
        return self.date.strftime("%b/%d/%Y")
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "location": self.location,
            "image": self.image.url,
            "club": self.club,
            "ticket_price": self.ticket_price,
            "duration": self.duration,
        }
    

class Tickets(models.Model):
    event=models.ForeignKey(Events,on_delete=models.CASCADE,related_name="event_tickets")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="tickets")
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.event} - {self.user} - {self.quantity} "
    
    def serialize(self):
        return {
            "id": self.id,
            "event": self.event.serialize(),
            "user": self.user.serialize(),
            "quantity": self.quantity,
            "date": self.event.date.strftime("%b %d %Y, %I:%M %p"),
        }
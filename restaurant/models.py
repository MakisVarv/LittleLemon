from django.db import models


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self):
        return self.first_name


# Add code to create Menu model
class MenuItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    inventory = models.SmallIntegerField()
    menu_item_description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return f"{self.title} : {str(self.price)}"

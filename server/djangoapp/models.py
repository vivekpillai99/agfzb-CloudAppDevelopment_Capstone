from django.db import models
from django.utils.timezone import now

SEDAN = 'sedan'
TYPES = [
    (SEDAN,'Sedan'),
    ('suv', 'SUV'), 
    ('wagon', 'WAGON')
]
# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default='Car Make')
    description = models.CharField(max_length=500)

    def __str__(self):
        return "This is a " + self.name + " with description: " + self.description 


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.CharField(null=False, max_length=100, default="Car Model")
    year = models.DateField()
    type = models.CharField(null=False, max_length=10, choices=TYPES, default=SEDAN)
    def __str__(self):
        return "This is a car of type " + self.name + " with dealerId: " + str(self.dealerId)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

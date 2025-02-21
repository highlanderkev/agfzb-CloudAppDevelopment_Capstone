from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    """
    Car Make model `class CarMake(models.Model)`
    - Name
    - Description
    - Any other fields you would like to include in car make model
    - __str__ method to print a car make object
    """
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=True, max_length=1000)

    def __str__(self):
        return f"Car Make: {self.name}"


class CarModel(models.Model):
    """
    Car Model model `class CarModel(models.Model):`:
    - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    - Name
    - Dealer id, used to refer a dealer created in cloudant database
    - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    - Year (DateField)
    - Any other fields you would like to include in car model
    - __str__ method to print a car make object
    """
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=True)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    type = models.CharField(null=False, max_length=20, choices=CAR_TYPE, default=SEDAN)
    year = models.DateField(null=False)

    def __str__(self):
        return f"Car Model: {self.name}"


class CarDealer:
    """
    Plain Python class `CarDealer` to hold dealer data
    - Dealer address
    - Dealer city
    - Dealer Full Name
    - Dealer id
    - Location lat
    - Location long
    - Dealer short name
    - Dealer state
    - Dealer zip
    """
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"

class DealerReview:
    """
    Plain Python class `DealerReview` to hold review data
    - dealership
    - name
    - purchase
    - review
    - purchase_date
    - car_make
    - car_model
    - car_year
    - sentiment
    - id
    """
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Dealer Review: {self.review}"

class SentimentAnalysis:
    """
    Plain Python class to hold sentiment analysis
    """
    def __init__(self, text, sentiment_score, sentiment_label):
        self.text = text
        self.sentiment_score = sentiment_score
        self.sentiment_label = sentiment_label
        
    def __str__(self):
        return f"Text: '{self.text}' | Sentiment: {self.sentiment_label}"
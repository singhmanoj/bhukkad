from django.db import models
from autoslug import AutoSlugField

class Cuisine(models.Model):
    """
    Store the multiple type of Cuisine like punjabi, italian etc
    """
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country)  # Country to which its associated
    is_active = models.BooleanField()          # To deactivate this Cuisine from the Projects
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)


class RestaurantModel(models.Model):
    """Restaurant Model for storing the Restaurant data
    """
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=name, unique=True)
    address = models.CharField(max_length=100)
    locality = models.ForeignKey(Locality)
    cuisines = models.ManyToManyField(Cuisine)   # Multiple Cusine options
    lat = models.CharField(max_length=10, default=None)
    long = models.CharField(max_length=10, default=None)
    do_delivery = models.BooleanField()
    is_active = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)
    rating = models.PositiveIntegerField()           # Total rating to get the Average Rating
    no_of_user_rated = models.PositiveIntegerField()  # Total no of user Rated
    elastic_sync = models.BooleanField()  # To track the syncing between Mysql and Elastic
    elastic_sync_time = models.DateField(null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def add_rating(self, rate):
        self.rating += rate
        self.no_of_user_rated += 1
        self.save(update_fields=['rating', 'no_of_user_rated'])

    def get_average_rating(self):
        if self.rating == 0:
            return 0
        else:
            return self.rating/float(self.no_of_user_rated)


class Locality(models.Model):
    """
    The region information added for the restaurant
    """
    locality = models.CharField(max_length=20, unique=True, db_index=True)
    city = models.ForeignKey(City)
    pincode = models.CharField(max_length=10)
    is_active = models.BooleanFaield()
    default_lat = models.CharField(max_length=10)
    default_long = models.CharField(max_length=10)


class City(models.Model):
    """
    City Information
    """
    name = models.CharField(max_length=20, unique=True, db_index=True)
    country = models.ForeignKey(Country)
    is_active = models.BooleanField()


class Country(models.Model):
    """
    Country information
    """
    name = models.CharField(max_length=20, unique=True, db_index=True)
    is_active = models.BooleanField()


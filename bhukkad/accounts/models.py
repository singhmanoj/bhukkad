from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from restaurant.models import RestaurantModel, Cuisine, City
from accounts.utils import get_moderated

# Create your models here.
GENDER_CHOICE = [
    ('M', 'MALE'),
    ('F', 'FEMALE')
]

RATING_CHOICES = [
    (1, 'Very Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
]


class CustomUserModel(AbstractBaseUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    lase_name = models.CharField(max_length=20)
    bio = models.TextField()
    birthday = models.DateField()
    # Here contact is True if we want to login via Phone No
    contact_no = models.CharField(max_length=15, unique=True)
    city = models.ForeignKey(City)
    gender = models.CharField(choices=GENDER_CHOICE)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    user_preference = models.ManyToManyField(Cuisine)

    USERNAME_FIELD = 'email'

    def get_excluded_restaurant(self):
        return UserRating.objects.filter(
            user=self, rated=1
        ).values_list('restaurant_id')

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name


class ReviewsModel(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    restaurant = models.ForeignKey(RestaurantModel)
    user = models.ForeignKey(CustomUserModel)
    is_moderated = models.BooleanField(default=False)  # For future purpose to block the abusive reviews
    created_on = models.DateField(auto_now_add=True)

    def get_moderated(self):
        self.is_moderated = get_moderated(self.title) and get_moderated(self.text)
        self.save(update_fields=['is_moderated'])

    class Meta:
        unique_together = (("restaurant", "user"),)


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    on_review = models.ForeignKey(ReviewsModel)
    user = models.ForeignKey(CustomUserModel)
    is_moderated = models.BooleanField()
    is_active = models.BooleanField(default=False)    # For future purpose to block the abusive reviews
    created_on = models.DateField(auto_now_add=True)


    def get_moderated(self):
        self.is_moderated = get_moderated(self.comment)
        self.save(update_fields=['is_moderated'])


class UserRating(models.Model):
    '''
    Have the User Rating.
    If User gives 1 rating simply means user doesn't want to see it in listing
    '''
    rated = models.IntegerField(choices=RATING_CHOICES)
    restaurant = models.ForeignKey(RestaurantModel)
    user = models.ForeignKey(CustomUserModel)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.restaurant.add_rating(self.rated)
        return super(UserRating, self).save(self, force_insert, force_update, using, update_fields)


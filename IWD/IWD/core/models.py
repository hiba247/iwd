from django.db import models

# Create your models here.

class Psychologist(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    phone_number = models.CharField()
    email = models.EmailField()
    
    def __str__(self):
        return f'Psychologist: {self.first_name} {self.last_name}'
    
class User(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    gender = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    anonymous = models.BooleanField()
    addiction = models.CharField()
    premium = models.CharField()
    streak = models.IntegerField()
    
    
    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'
    

class Habit_Collection(models.Model):
    pass

class Habit(models.Model):
    title = models.TextField()
    done_for_the_day = models.BooleanField()
    habit_collection = models.ForeignKey(Habit_Collection, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Habit: {self.description}'
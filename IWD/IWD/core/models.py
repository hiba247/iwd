from django.db import models

# Create your models here.

class Psychologist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return f'Psychologist: {self.first_name} {self.last_name}'
    
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    anonymous = models.BooleanField()
    addiction = models.CharField(max_length=100)
    premium = models.CharField(max_length=100)
    streak = models.IntegerField()
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'
    

class Habit_Collection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    streak_continued = models.BooleanField()
    
    def __str__(self):
        return f'Habits of {self.created_at}'
    

class Habit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    done_for_the_day = models.BooleanField()
    habit_collection = models.ForeignKey(Habit_Collection, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Habit: {self.description}'
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    upvote_count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Post titled: {self.title}'
    
    
class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Comment:{self.content} made by {self.user}'
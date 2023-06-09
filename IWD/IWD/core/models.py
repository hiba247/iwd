from django.db import models
from django.contrib.auth.models import AbstractUser

"""
This is where the models are defined, the definitions are self-evident with clear names
"""

# An entity representing a psychologist offering his services on the website
class Psychologist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='psychologists', null=True)
    accepted = models.BooleanField(default=False)       # A psychologist won't be accepted to have any patients unless approved by an admin (accepted == True)
    
    def __str__(self):
        return f'Psychologist: {self.first_name} {self.last_name}'
    

# An authenticated user in the website
class User(AbstractUser):
    
    username=None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    addiction = models.CharField(max_length=100)
    premium = models.BooleanField(default=False)
    streak = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='avatars', null=True)
    #premium features
    frequency_of_use = models.CharField(max_length=100)
    cause_of_addiction = models.CharField(max_length=100)
    assigned_psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'
    

# An entity representing a post made by a user    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    upvote_count = models.IntegerField(default=0)
    upvoters = models.ManyToManyField(User, related_name='upvoters')
    photo = models.ImageField(upload_to='posts_images', null=True)
    anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    
    def __str__(self):
        return f'Post titled: {self.title}'
    

# An entiy representing a comment made on a post    
class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Comment:{self.content} made by {self.user}'
    

# An entity representing an event for the users, made by the admin    
class Event(models.Model):
    price=models.FloatField()
    place=models.CharField(max_length=100)
    num_places=models.IntegerField()
    description = models.TextField()
    date = models.DateField()
    categorie = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='events', null=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Event: {self.description}'
    

# An entity representing a formation held on the website in which users can enroll    
class Formation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    teacher = models.CharField(max_length=100)
    enrollers = models.ManyToManyField(User)
    
    def __str__(self):
        return f'Formation {self.title}'
    

# An entity representing an admin    
class Admin(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Admin: {self.first_name} {self.last_name}'
    

# An entity representing a task assigned to the user by his psychologist on the website   
class Task(models.Model):
    description = models.CharField(max_length=100)
    progress = models.FloatField(default=0)
    goal = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Task: {self.description}'
    

# An entity representing articles added by the admin to the website    
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    added_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Article: {self.title}'
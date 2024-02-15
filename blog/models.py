from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Define a Post model for representing blog posts in the database.
class Post(models.Model):
    title = models.CharField(max_length=100)
    
    # A TextField for the post's content, which can contain an unlimited number of characters.
    content = models.TextField()  

    # A DateTimeField for the date and time the post was created.
    # Default value is set to the current date and time when a post instance is created.
    date_posted = models.DateTimeField(default=timezone.now)
    
    # A ForeignKey linking the post to a user.
    # on_delete=models.CASCADE means that if the referenced user is deleted, the post will also be deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # The __str__ method returns the post title, which is helpful for representing the object in the admin interface or shell.
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) # Return the URL to the post detail page for the post with the primary key (pk) of self.

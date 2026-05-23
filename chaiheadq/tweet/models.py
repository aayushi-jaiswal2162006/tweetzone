from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    photo = models.ImageField(upload_to='tweet_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Tweet"

    def total_likes(self):
        return self.likes.count()


    



class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Optional: add profile photo field here if needed later

    def __str__(self):
        return f'Profile of {self.user.username}'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
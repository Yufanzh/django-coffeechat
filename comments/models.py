from django.contrib.auth.models import User
from django.db import models
from tweets.models import Tweet
from likes.models import Likes
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Comment(models.Model):
    """
    this is a simple version of comment function
    can only comment on a tweet, not the comments of the tweet
    """
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # we need to sort comments under one tweet
        index_together = (('tweet', 'created_at'),)
    
    @property
    def like_set(self):
        return Likes.objects.filter(
            content_type = ContentType.objects.get_for_model(Comment),
            object_id = self.id,
        ).order_by('-created_at')
    
    def __str__(self):
        return '{} - {} says {} at tweet {}'.format(
            self.created_at,
            self.user,
            self.content,
            self.tweet_id,
        )
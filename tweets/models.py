from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from likes.models import Likes
from utils.time_helpers import utc_now
from tweets.constants import TweetPhotoStatus, TWEET_PHOTO_STATUS_CHOICES

class Tweet(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        help_text='who posts this tweet',
    ) # better coding style
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')
    

    @property
    def hours_to_now(self):
        return (utc_now() - self.created_at).seconds // 3600

    @property
    def like_set(self):
        return Likes.objects.filter(
            content_type = ContentType.objects.get_for_model(Tweet),
            object_id = self.id,
        ).order_by('-created_at')
    
    def __str__(self):
        # print an instance, we print the __str__ instead.
        return f'{self.created_at}{self.user}: {self.content}'

class TweetPhoto(models.Model):
    # photos under which tweet
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)

    # who uploaded the photos, we create a user to avoid more join query
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # photos file
    file = models.FileField()
    order = models.IntegerField(default=0)

    # photo status, used for checking
    status = models.IntegerField(
        default=TweetPhotoStatus.PENDING,
        choices=TWEET_PHOTO_STATUS_CHOICES,
    )

    # soft delete mark, asynchronize can make it more efficient
    has_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('user', 'created_at'), # search for photos posted by one user
            ('has_deleted', 'created_at'), # search recent deleted photos
            ('status', 'created_at'), # search photos status
            ('tweet', 'order'), # most common one, search for tweet list by order
        )
    
    def __str__(self):
        return f'{self.tweet_id}: {self.file}'


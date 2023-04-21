from accounts.services import UserService
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField() # comment id or tweet id
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null = True,
    )
    # user liked contente_object at created_at
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # here we use unique together, which will create a 
        # <user, content_type, object_id> index
        # this can be used to search certain user like which different objects
        unique_together = (('user', 'content_type', 'object_id'),)
        # this index is used to sort in time all the likes of a content_object
        index_together = (('content_type', 'object_id', 'created_at'),)

    def __str__(self):
        return '{} - {} liked {} {}'.format(
            self.created_at,
            self.user,
            self.content_type,
            self.object_id,
        )
    
    @property
    def cached_user(self):
        return UserService.get_user_through_cache(self.user_id)



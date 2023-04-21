from accounts.services import UserService
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from friendships.listeners import friendship_changed

# Create your models here.
class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'following_friendship_set',
    )
    to_user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'follower_friendship_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            # get all my followings, chronological order
            ('from_user_id', 'created_at'),
            # get all my followers, chronological order
            ('to_user_id', 'created_at'),
        )
        unique_together = (('from_user_id', 'to_user_id'),)
    
    def __str__(self):
        return '{} followed {}'.format(self.from_user_id, self.to_user_id)
    
    @property
    def cached_from_user(self):
        return UserService.get_user_through_cache(self.from_user_id)
    
    @property
    def cached_to_user(self):
        return UserService.get_user_through_cache(self.to_user_id)
    
# hook up with listeners to invalidate cache
pre_delete.connect(friendship_changed, sender=Friendship)
post_save.connect(friendship_changed, sender=Friendship)
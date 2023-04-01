from django.db import models
from django.contrib.auth.models import User

# create your models here.
class UserProfile(models.Model):
    # One2One field will conreate a unique index, to make sure there won;t
    # be multiple userprofiles pointing to one user
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # use FileField is better than ImageField
    avatar = models.FileField(null=True)
    # when a user is created, we will creat a user profile's object
    # current user doesn't have time to set nicknames etc, so we set default to null
    nickname = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)

    # define a profile property to put in user model
    # then when we visit profile, user_instance.profile
    # we can apply get_or_create in userprofile to get the profile object
    def get_profile(user):
        if hasattr(user, '_cached_user_profile'):
            return getattr(user, '_cached_user_profile')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        # use user object to cache, to avoid repeated query in database
        setattr(user, '_cached_user_profile', profile)
        return profile

    # put a profile property for quick visit
    User.profile = property(get_profile)
# Create your models here.

from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import caches
from coffeechat.cache import USER_PROFILE_PATTERN

cache = caches['testing'] if settings.TESTING else caches['default']

class UserService:
    
    @classmethod
    def get_profile_through_cache(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id=user_id)

        # read from cache first
        profile = cache.get(key)
        # cache hit return
        if profile is not None:
            return profile
        
        # cache miss, read from db
        profile, _ = UserProfile.objects.get_or_create(user_id=user_id)
        cache.set(key, profile)
        return profile
    
    @classmethod
    def invalidate_profile(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id=user_id)
        cache.delete(key)

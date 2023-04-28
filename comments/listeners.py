from utils.listeners import invalidate_object_cache
from utils.redis_helper import RedisHelper

def incr_comments_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F
    # F directly write to db
    # F() together with update can optimize efficiency,
    # no need to use get() and save()

    if not created:
        return
    
    # handle new comment
    Tweet.objects.filter(id=instance.tweet_id)\
        .update(comments_count=F('comments_count') + 1)
    RedisHelper.incr_count(instance.tweet, 'comments_count')

def decr_comments_count(sender, instance, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F 

    # handle comment deletion
    Tweet.objects.filter(id=instance.tweet_id)\
        .update(comments_count=F('comments_count') - 1)
    RedisHelper.decr_count(instance.tweet, 'comments_count')

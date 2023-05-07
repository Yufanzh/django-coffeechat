from newsfeeds.models import NewsFeed
from newsfeeds.tasks import fanout_newsfeeds_main_task
from coffeechat.cache import USER_NEWSFEEDS_PATTERN
from utils.redis_helper import RedisHelper

class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        # this sentence is to: create a fanout task under celery configured message queue
        # param: tweet, any worker process monitoring the message queue will have the chance to get this task
        # worker process will exercise fanout_newsfeeds_task code to get async tasks
        # if process this task needs 10s, then it will spend on the worker process, not during client post tweet
        # so .delay will exercise immediately, user won't feel
        # delay params must be something that celery can serialize. so we can only pass tweet.id, not tweet itself
        # because celery doesn't know how to serialize Tweet.
        
        fanout_newsfeeds_main_task.delay(tweet.id, tweet.user_id)

    @classmethod
    def get_cached_newsfeeds(cls, user_id):
        # lazy loading
        queryset = NewsFeed.objects.filter(user_id=user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=user_id)
        return RedisHelper.load_objects(key, queryset)

    @classmethod
    def push_newsfeed_to_cache(cls, newsfeed):
        # queryset is lazy loading
        queryset = NewsFeed.objects.filter(user_id=newsfeed.user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=newsfeed.user_id)
        RedisHelper.push_object(key, newsfeed, queryset)
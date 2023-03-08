from friendships.services import FriendshipService
from newsfeeds.models import NewsFeed

class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        followers = FriendshipService.get_followers(tweet.user)
        # for + query will be very slow, not encouraged by production
        # for follower in followers:
        #     NewsFeed.objects.create(user=follower, tweet=tweet)
        # django method -- bulk_create!
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        # append yourself
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeeds)




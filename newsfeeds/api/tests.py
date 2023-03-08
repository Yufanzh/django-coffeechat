from newsfeeds.models import NewsFeed
from newsfeeds.services import NewsFeedService
from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase


NEWSFEEDS_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'

class NewsFeedApiTests(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.linghu = self.create_user('linghu')
        self.linghu_client = APIClient()
        self.linghu_client.force_authenticate(self.linghu)

        self.dongxie = self.create_user('dongxie')
        self.dongxie_client = APIClient()
        self.dongxie_client.force_authenticate(self.dongxie)

        # create followings and followers for dongxie
        for i in range(2):
            follower = self.create_user('dongxie_follower{}'.format(i))
            self.create_friendship(from_user=follower, to_user=self.dongxie)
        for i in range(3):
            following = self.create_user('dongxie_following{}'.format(i))
            self.create_friendship(from_user=self.dongxie, to_user=following)

    def test_list(self):
        # need login
        response = self.anonymous_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 403)
        # use get
        response = self.linghu_client.post(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 405)
        # start with nothing
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 200)
        # print("what's the response data?", response.data)
        self.assertEqual(len(response.data['newsfeeds']), 0)
        # can see your own tweets
        self.linghu_client.post(POST_TWEETS_URL, {'content': 'Hello World'})
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['newsfeeds']), 1)
        # see your followings' tweets
        self.linghu_client.post(FOLLOW_URL.format(self.dongxie.id))
        response = self.dongxie_client.post(POST_TWEETS_URL, {
            'content': 'Hello Twitter',
        })
        posted_tweet_id = response.data['id']
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['newsfeeds']), 2)
        self.assertEqual(response.data['newsfeeds'][0]['tweet']['id'], posted_tweet_id)



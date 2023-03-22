from datetime import timedelta
from utils.time_helpers import utc_now
from testing.testcases import TestCase


# Create your tests here.
class TweetTests(TestCase):
    def setUp(self):
        self.alex = self.create_user('alex')
        self.tweet = self.create_tweet(self.alex, content='This is my first tweet!')

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now, 10)

    def test_like_set(self):
        self.create_like(self.alex, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(self.alex, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        dongxie = self.create_user('dongxie')
        self.create_like(dongxie, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)

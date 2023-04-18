from testing.testcases import TestCase
from rest_framework.test import APIClient

LIKE_BASE_URL = '/api/likes/'
LIKE_CANCEL_URL = '/api/likes/cancel/'
COMMENT_LIST_API = '/api/comments/'
TWEET_DETAIL_API = '/api/tweets/{}/'
TWEET_LIST_API = '/api/tweets/'
NEWSFEED_LIST_API = '/api/newsfeeds/'


class LikeApiTests(TestCase):

    def setUp(self):
        self.linghu, self.linghu_client = self.create_user_and_client('linghu')
        self.dongxie, self.dongxie_client = self.create_user_and_client('dongxie')
        self.anonymous_client = APIClient()
    
    def test_tweet_likes(self):
        tweet = self.create_tweet(self.linghu)
        data = {'content_type': 'tweet', 'object_id': tweet.id}

        # anonymous is not allowed
        response = self.anonymous_client.post(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 403)

        # get is not allowed
        response = self.linghu_client.get(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 405)

        # wrong content_type
        response = self.linghu_client.post(LIKE_BASE_URL, {
            'content_type': 'twitter',
            'object_id': tweet.id,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('content_type' in response.data['errors'], True)

        # wrong object id
        response = self.linghu_client.post(LIKE_BASE_URL, {
            'content_type': 'tweet',
            'object_id': -1,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('object_id' in response.data['errors'], True)

        # post success
        response = self.linghu_client.post(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(tweet.like_set.count(), 1)

        # duplicate likes
        self.linghu_client.post(LIKE_BASE_URL, data)
        self.assertEqual(tweet.like_set.count(), 1)
        self.dongxie_client.post(LIKE_BASE_URL, data)
        self.assertEqual(tweet.like_set.count(), 2)

    
    def test_comment_likes(self):
        tweet = self.create_tweet(self.linghu)
        comment = self.create_comment(self.dongxie, tweet)
        data = {'content_type': 'comment', 'object_id': comment.id}

        # anonymous is not allowed
        response = self.anonymous_client.post(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 403)

        # get is not allowed
        response = self.linghu_client.get(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 405)

        # wrong content_type
        response = self.linghu_client.post(LIKE_BASE_URL, {
            'content_type': 'coment',
            'object_id': comment.id,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('content_type' in response.data['errors'], True)

        # wrong object id
        response = self.linghu_client.post(LIKE_BASE_URL, {
            'content_type': 'comment',
            'object_id': -1,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('object_id' in response.data['errors'], True)

        # post success
        response = self.linghu_client.post(LIKE_BASE_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(comment.like_set.count(), 1)

        # duplicate likes
        self.linghu_client.post(LIKE_BASE_URL, data)
        self.assertEqual(comment.like_set.count(), 1)
        self.dongxie_client.post(LIKE_BASE_URL, data)
        self.assertEqual(comment.like_set.count(), 2)
    
    def test_cancel(self):
        tweet = self.create_tweet(self.linghu)
        comment = self.create_comment(self.dongxie, tweet)
        like_comment_data = {'content_type': 'comment', 'object_id': comment.id}
        like_tweet_data = {'content_type': 'tweet', 'object_id': tweet.id}
        self.linghu_client.post(LIKE_BASE_URL, like_comment_data)
        self.dongxie_client.post(LIKE_BASE_URL, like_tweet_data)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 1)

        # login required
        response = self.anonymous_client.post(LIKE_CANCEL_URL,  like_comment_data)
        self.assertEqual(response.status_code, 403)

        # get not allowed
        response = self.linghu_client.get(LIKE_CANCEL_URL, like_comment_data)
        self.assertEqual(response.status_code, 405)  

        # wrong content_type      
        response = self.linghu_client.post(LIKE_CANCEL_URL, {
            'content_type': 'wrong',
            'object_id': 1,
        })
        self.assertEqual(response.status_code, 400)

        # wrong object id
        response = self.linghu_client.post(LIKE_CANCEL_URL, {
            'content_type': 'comment',
            'object_id': -1,
        })
        self.assertEqual(response.status_code, 400)

        # dongxie has not liked before, not a problem
        response = self.dongxie_client.post(LIKE_CANCEL_URL, like_comment_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], False)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 1)

        # successfully canceled
        response = self.linghu_client.post(LIKE_CANCEL_URL, like_comment_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], True)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 0)

        # linghu has not liked before, not a problem
        response = self.linghu_client.post(LIKE_CANCEL_URL, like_tweet_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], False)
        self.assertEqual(tweet.like_set.count(), 1)
        self.assertEqual(comment.like_set.count(), 0)

        # dongxie's like has been canceled
        response = self.dongxie_client.post(LIKE_CANCEL_URL, like_tweet_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], True)
        self.assertEqual(tweet.like_set.count(), 0)
        self.assertEqual(comment.like_set.count(), 0)       
    
    def test_likes_in_comments_api(self):
        tweet = self.create_tweet(self.linghu)
        comment = self.create_comment(self.linghu, tweet)

        # test anonymous
        response = self.anonymous_client.get(COMMENT_LIST_API, {'tweet_id': tweet.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comments'][0]['has_liked'], False)
        self.assertEqual(response.data['comments'][0]['likes_count'], 0)

        # test comments list api
        response = self.dongxie_client.get(COMMENT_LIST_API, {'tweet_id': tweet.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comments'][0]['has_liked'], False)
        self.assertEqual(response.data['comments'][0]['likes_count'], 0)
        self.create_like(self.dongxie, comment)
        response = self.dongxie_client.get(COMMENT_LIST_API, {'tweet_id': tweet.id})
        self.assertEqual(response.data['comments'][0]['has_liked'], True)
        self.assertEqual(response.data['comments'][0]['likes_count'], 1)

        # test tweet detail api
        self.create_like(self.linghu, comment)
        url = TWEET_DETAIL_API.format(tweet.id)
        response = self.dongxie_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comments'][0]['has_liked'], True)
        self.assertEqual(response.data['comments'][0]['likes_count'], 2)
    
    def test_likes_in_tweets_api(self): 
         tweet = self.create_tweet(self.linghu)

         # test tweet detail api
         url = TWEET_DETAIL_API.format(tweet.id)
         response = self.anonymous_client.get(url)
         # test anonymous
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.data['has_liked'], False)
         self.assertEqual(response.data['likes_count'], 0)
    
         response = self.dongxie_client.get(url)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.data['has_liked'], False)
         self.assertEqual(response.data['likes_count'], 0)         
         self.create_like(self.dongxie, tweet)
         response = self.dongxie_client.get(url)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.data['has_liked'], True)
         self.assertEqual(response.data['likes_count'], 1)

         # test tweets list api
         response = self.dongxie_client.get(TWEET_LIST_API, {'user_id': self.linghu.id})
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.data['results'][0]['has_liked'], True)
         self.assertEqual(response.data['results'][0]['likes_count'], 1)

         # test newsfeed list api
         self.create_like(self.linghu, tweet)
         self.create_newsfeed(self.dongxie, tweet)     
         response = self.dongxie_client.get(NEWSFEED_LIST_API)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.data['results'][0]['tweet']['has_liked'], True)
         self.assertEqual(response.data['results'][0]['tweet']['likes_count'], 2)

         # test likes details
         url = TWEET_DETAIL_API.format(tweet.id)
         response = self.dongxie_client.get(url)
         self.assertEqual(len(response.data['likes']), 2)
         self.assertEqual(response.data['likes'][0]['user']['id'], self.linghu.id)
         self.assertEqual(response.data['likes'][1]['user']['id'], self.dongxie.id)

       






from notifications.models import Notification
from testing.testcases import TestCase
from rest_framework.test import APIClient

COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'
NOTIFICATION_URL = '/api/notifications/'

class NotificationTests(TestCase):

    def setUp(self):
        self.clear_cache()
        self.linghu, self.linghu_client = self.create_user_and_client('linghu')
        self.dongxie, self.dongxie_client = self.create_user_and_client('dongxie')
        self.dongxie_tweet = self.create_tweet(self.dongxie)

    def test_comment_create_api_trigger_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.linghu_client.post(COMMENT_URL, {
            'tweet_id': self.dongxie_tweet.id,
            'content': 'a ha',
        })
        self.assertEqual(Notification.objects.count(), 1)

    def test_like_create_api_trigger_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.linghu_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.dongxie_tweet.id,
        })
        self.assertEqual(Notification.objects.count(), 1)        


class NotificationsAPITests(TestCase):
    def setUp(self):
        self.linghu, self.linghu_client = self.create_user_and_client('linghu')
        self.dongxie, self.dongxie_client = self.create_user_and_client('dongxie')
        self.linghu_tweet = self.create_tweet(self.linghu)
    
    def test_unread_count(self):
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.linghu_tweet.id,
        })

        url = '/api/notifications/unread-count/'
        response = self.linghu_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['unread_count'], 1)

        comment = self.create_comment(self.linghu, self.linghu_tweet)
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': comment.id,
        })
        response = self.linghu_client.get(url)
        self.assertEqual(response.data['unread_count'], 2)
        response = self.dongxie_client.get(url)
        self.assertEqual(response.data['unread_count'], 0)

    def test_mark_all_as_read(self):
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.linghu_tweet.id,    
        })
        comment = self.create_comment(self.linghu, self.linghu_tweet)
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': comment.id,
        })

        unread_url = '/api/notifications/unread-count/'
        response = self.linghu_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 2)
        response = self.dongxie_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 0)

        mark_url = '/api/notifications/mark-all-as-read/'
        response = self.linghu_client.get(mark_url)
        self.assertEqual(response.status_code, 405)

        # dongxie cannot mark linghu's notification as read
        response = self.dongxie_client.post(mark_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['marked_count'], 0)

        # linghu can mark his own notification as read
        response = self.linghu_client.post(mark_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['marked_count'], 2)
        response = self.linghu_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 0)
    
    def test_list(self):
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.linghu_tweet.id,
        })
        comment = self.create_comment(self.linghu, self.linghu_tweet)
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': comment.id,
        })

        # anonymous cannot access api
        response = self.anonymous_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, 403)
        # dongxie cannot see any notifications
        response = self.dongxie_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        # linghu can see two
        response = self.linghu_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

        # after mark, one unread notification
        notification = self.linghu.notifications.first()
        notification.unread = False
        notification.save()
        response = self.linghu_client.get(NOTIFICATION_URL)
        self.assertEqual(response.data['count'], 2)
        response = self.linghu_client.get(NOTIFICATION_URL, {'unread': True})
        self.assertEqual(response.data['count'], 1)
        response = self.linghu_client.get(NOTIFICATION_URL, {'unread': False})
        self.assertEqual(response.data['count'], 1)

    def test_update(self):
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.linghu_tweet.id,
        })
        comment = self.create_comment(self.linghu, self.linghu_tweet)
        self.dongxie_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': comment.id,
        })
        notification = self.linghu.notifications.first()

        url = '/api/notifications/{}/'.format(notification.id)
        # cannot post, only put
        response = self.dongxie_client.post(url, {'unread': False})
        self.assertEqual(response.status_code, 405)
        # cannot change by others update
        response = self.anonymous_client.put(url, {'unread': False})
        self.assertEqual(response.status_code, 403)
        # because queryset is based on current user, so it will return 404 not 403
        response = self.dongxie_client.put(url, {'unread': False})
        self.assertEqual(response.status_code, 404)
        # mark as read successfully
        response = self.linghu_client.put(url, {'unread': False})
        self.assertEqual(response.status_code, 200)
        unread_url = '/api/notifications/unread-count/'
        response = self.linghu_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 1)

        # mark as unread
        response = self.linghu_client.put(url, {'unread': True})
        response = self.linghu_client.get(unread_url)
        self.assertEqual(response.data['unread_count'], 2)

        # must have unread
        response = self.linghu_client.put(url, {'verb': 'newverb'})
        self.assertEqual(response.status_code, 400)
        # cannot update other information
        response = self.linghu_client.put(url, {'verb': 'newverb', 'unread': False})
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertNotEqual(notification.verb, 'newverb')









        
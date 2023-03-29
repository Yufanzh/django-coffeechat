from testing.testcases import TestCase
from inbox.services import NotificationService
from notifications.models import Notification

# Create your tests here.
class NotificationServiceTests(TestCase):

    def setUp(self):
        self.linghu = self.create_user('linghu')
        self.dongxie = self.create_user('dongxie')
        self.linghu_tweet = self.create_tweet(self.linghu)
    
    def test_send_comment_notification(self):
        # do not dispatch notification if tweet user == comment user
        comment = self.create_comment(self.linghu, self.linghu_tweet)
        NotificationService.send_comment_notification(comment)
        self.assertEqual(Notification.objects.count(), 0)

        # dispatch notification if tweet user != comment user
        comment = self.create_comment(self.dongxie, self.linghu_tweet)
        NotificationService.send_comment_notification(comment)
        self.assertEqual(Notification.objects.count(), 1)        
    
    def test_send_like_notification(self):
        # do not dispatch notification if tweet user == like user
        like = self.create_like(self.linghu, self.linghu_tweet)
        NotificationService.send_like_notification(like)
        self.assertEqual(Notification.objects.count(), 0)

        # dispatch notification if tweet user != like user
        like = self.create_like(self.dongxie, self.linghu_tweet)
        NotificationService.send_like_notification(like)
        self.assertEqual(Notification.objects.count(), 1)
        
          
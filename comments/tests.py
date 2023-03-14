from testing.testcases import TestCase

# Create your tests here.
class CommentModelTests(TestCase):

    def test_comment(self):
        user = self.create_user('Alex')
        tweet = self.create_tweet(user)
        comment = self.create_comment(user, tweet)
        self.assertNotEqual(comment.__str__(), None)
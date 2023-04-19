from friendships.models import Friendship
from friendships.services import FriendshipService
from testing.testcases import TestCase

# Create your tests here.
class FriendshipServiceTests(TestCase):

    def setUp(self):
        self.clear_cache()
        self.linghu = self.create_user('linghu')
        self.dongxie = self.create_user('dongxie')

    def test_get_following(self):
        user1 = self.create_user('user1')
        user2 = self.create_user('user2')
        for to_user in [user1, user2, self.dongxie]:
            Friendship.objects.create(from_user=self.linghu, to_user=to_user)
        FriendshipService.invalidate_following_cache(self.linghu.id)

        user_id_set = FriendshipService.get_following_user_id_set(self.linghu.id)
        self.assertSetEqual(user_id_set, {user1.id, user2.id, self.dongxie.id})

        Friendship.objects.filter(from_user=self.linghu, to_user=self.dongxie).delete()
        FriendshipService.invalidate_following_cache(self.linghu.id)
        user_id_set = FriendshipService.get_following_user_id_set(self.linghu.id)
        self.assertSetEqual(user_id_set, {user1.id, user2.id})

from friendships.models import Friendship

class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):
        # correct way, use two queries to avoid N queries to database
        # approach 1
        # friendships = Friendship.objects.filter(to_user = user)
        # follower_ids = [friendship.from_user_id for friendship in friendships]
        # followers = User.object.filter(id__in=follower_ids)
        # approach 2 - prefetch
        friendships = Friendship.objects.filter(
            to_user=user,
        ).prefetch_related('from_user')
        return [friendship.from_user for friendship in friendships]
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

    @classmethod
    def get_following_user_id_set(cls, from_user_id):
        key = FOLLOWING_PATTERN.format(user_id=from_user_id)
        user_id_set = cache.get(key)
        if user_id_set is not None:
            return user_id_set
        
        friendships = Friendship.objects.filter(from_user_id=from_user_id)
        user_id_set = set([
            fs.to_user_id
            for fs in friendships
        ])
        cache.set(key, user_id_set)
        return user_id_set
    
    @classmethod
    def has_followed(cls, from_user, to_user):
        return Friendship.objects.filter(
            from_user = from_user,
            to_user = to_user,
        ).exists()
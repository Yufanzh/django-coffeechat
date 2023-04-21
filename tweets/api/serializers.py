from accounts.api.serializers import UserSerializerForTweet
from comments.api.serializers import CommentSerializer
from likes.api.serializers import LikeSerializer
from likes.services import LikeService
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.constants import TWEET_PHOTOS_UPLOAD_LIMIT
from tweets.models import Tweet
from tweets.services import TweetService

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet(source='cached_user')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    photo_urls = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id', 
            'user', 
            'created_at', 
            'content',
            'comments_count',
            'likes_count',
            'has_liked',
            'photo_urls',
            )
    
    def get_likes_count(self, obj):
        return obj.like_set.count()
    
    def get_comments_count(self, obj):
        return obj.comment_set.count() #django automatically has this set
    
    def get_has_liked(self, obj):
        # current logged in user
        return LikeService.has_liked(self.context['request'].user, obj)
    
    def get_photo_urls(self, obj):
        photo_urls = []
        for photo in obj.tweetphoto_set.all().order_by('order'):
            photo_urls.append(photo.file.url)
        return photo_urls

class TweetSerializerForDetail(TweetSerializer):
    comments = CommentSerializer(source='comment_set', many=True)
    likes = LikeSerializer(source='like_set', many=True)

    class Meta:
        model = Tweet
        fields = (
            'id', 
            'user', 
            'comments', 
            'created_at', 
            'content',
            'likes',
            'comments',
            'likes_count',
            'comments_count',
            'has_liked',
            'photo_urls',
        )
    
    
class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)
    files = serializers.ListField(
        child = serializers.FileField(),
        allow_empty = True,
        required = False,
    )

    class Meta:
        model = Tweet
        fields = ('content', 'files')
    
    def validate(self, data):
        if len(data.get('files', [])) > TWEET_PHOTOS_UPLOAD_LIMIT:
            raise ValidationError({
                'message': f'You can upload {TWEET_PHOTOS_UPLOAD_LIMIT} photos '
                            'at most'
            })
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        if validated_data.get('files'):
            TweetService.create_photos_from_files(
                tweet,
                validated_data['files'],
            )
        return tweet




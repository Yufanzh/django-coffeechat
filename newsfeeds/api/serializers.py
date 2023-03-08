from rest_framework import serializers
from newsfeeds.models import NewsFeed
from tweets.api.serializers import TweetSerializer
from tweets.models import Tweet

class NewsFeedSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = NewsFeed
        fields = ('id', 'created_at', 'user', 'tweet')
    
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_tweet(self, tweet_id):
        pass
    
    def get_created_at(self, obj):
        return obj.created_at
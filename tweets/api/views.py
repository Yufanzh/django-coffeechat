from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate
from tweets.models import Tweet

class TweetViewSet(viewsets.GenericViewSet):
    # queryset = Tweet.objects.all()
    serializer_class = TweetSerializerForCreate

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()] # list func can be accessed by anyone
        return [IsAuthenticated()]

    def list(self, request):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        
        # not eligate way
        #tweets = Tweet.objects.filter(
        #    user_id = request.query_params['user_id']
        #).order_by('-created_at') # from newest to oldest
        user_id = request.query_params['user_id']
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response({'tweets': serializer.data}) # rules to return as dictionary for JSON format
    
    def create(self, request):
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        # save will trigger create method in TweetSerializerForCreate
        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data, status=201)


    
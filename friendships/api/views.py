from django.contrib.auth.models import User
from friendships.api.paginations import FriendshipPagination
from friendships.models import Friendship
from friendships.services import FriendshipService
from friendships.api.serializers import (
    FollowingSerializer,
    FollowerSerializer,
    FriendshipSerializerForCreate,
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response



class FriendshipViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    # different view should have different pagination rules
    pagination_class = FriendshipPagination
    
    # GET /api/friendships/1/followers/ --> 1: pk
    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        # pk --> primary key
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowerSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        # pk --> primary key
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowingSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    
    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        # edge case: multi-follow at the same person
        # if already followed, return 201
        if Friendship.objects.filter(from_user=request.user, to_user = pk).exists():
            return Response({
                'success': True,
                'duplicate': True,
            }, status=status.HTTP_201_CREATED)
        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': pk,
        })
        # if pk is not reasonable, return 400 BAD REQUEST
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        # Attention!! pk is a str not int
        if request.user.id == int(pk):
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself',
            }, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = Friendship.objects.filter(
            from_user = request.user,
            to_user = pk,
        ).delete()
        return Response({'success': True, 'deleted': deleted})




            
    

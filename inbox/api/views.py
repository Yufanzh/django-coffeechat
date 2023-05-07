from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from inbox.api.serializers import (
    NotificationSerializer,
    NotificationSerializerForUpdate,
)
from django_ratelimit.decorators import ratelimit
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.decorators import required_params

class NotificationViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('unread',)

    def get_queryset(self):
        return self.request.user.notifications.all()
        # another way
        # return Notification.objects.filter(recipient=self.request.user)
    
    @action(methods=['GET'], detail=False, url_path='unread-count')
    @method_decorator(ratelimit(key='user', rate='3/s', method='GET', block=True))
    def unread_count(self, request, *args, **kwargs):
        # GET /api/notifications/unread-count/ # use - not _
        count = self.get_queryset().filter(unread=True).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False, url_path='mark-all-as-read')
    @method_decorator(ratelimit(key='user', rate='3/s', method='POST', block=True))
    def mark_all_as_read(self, request, *args, **kwargs):
        updated_count = self.get_queryset().update(unread=False)
        return Response({'marked_count': updated_count}, status=status.HTTP_200_OK)
    

    @required_params(method='PUT', params=['unread'])
    @method_decorator(ratelimit(key='user', rate='3/s', method='POST', block=True))
    def update(self, request, *args, **kwargs):
        # PUT '/api/notifications/1/'
        """
        user can mark a notification as unread or read, doing that count as
        an update to notification. so we can just reinstall update method
        another way to do that is to create func mark_as_read, mark_as_unread
        """
        serializer = NotificationSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        notification = serializer.save()
        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_200_OK,
        )
    
    
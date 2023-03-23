from likes.api.serializers import (
    LikeSerializer,
    LikeSerializerForCreate,
)
from likes.models import Likes
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.decorators import required_params

class LikeViewSet(viewsets.GenericViewSet):
    queryset = Likes.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_classes = LikeSerializerForCreate

    @required_params(request_attr='data', params=['content_type', 'object_id'])
    def create(self, request, *args, **kwargs):
        serializer = LikeSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        return Response(
            LikeSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )
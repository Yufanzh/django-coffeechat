from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from utils.permissions import IsObjectOwner
from utils.decorators import required_params
from inbox.services import NotificationService


class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现 list, create, update, destroy 的方法
    不实现 retrieve（查询单个 comment） 的方法，因为没这个需求
    """
    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id',)
    # POST /api/comments/ -> create
    # GET /api/comments/ -> list
    # GET /api/comments/1/ -> retrieve
    # DELETE /api/comments/1/ -> destroy
    # PATCH /api/comments/1/ -> partial_update
    # PUT /api/comments/1/ -> update

    def get_permissions(self):
        # 注意要加用 AllowAny() / IsAuthenticated() 实例化出对象
        # 而不是 AllowAny / IsAuthenticated 这样只是一个类名
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsObjectOwner()]
        return [AllowAny()]
    
    @required_params(params=['tweet_id'])
    def list(self, request, *args, **kwargs):
        
        # filter method 1
        # tweet_id = request.query_params['tweet_id']
        # comments = Comment.objects.filter(tweet_id=tweet_id)
        # filter method 2
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).prefetch_related('user').order_by('created_at')
        serializer = CommentSerializer(
            comments, 
            context = {'request': request},
            many=True,
        )
        return Response(
            {'comments': serializer.data}, 
            status=status.HTTP_200_OK,
        ) 
    


    def create(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # 注意这里必须要加 'data=' 来指定参数是传给 data 的
        # 因为默认的第一个参数是 instance
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save 方法会触发 serializer 里的 create 方法，点进 save 的具体实现里可以看到
        comment = serializer.save()
        NotificationService.send_comment_notification(comment)
        return Response(
            CommentSerializer(comment, context = {'request': request}).data,  
            status=status.HTTP_201_CREATED,
        )
    
    def update(self, request, *args, **kwargs):
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            raise Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()
        return Response(
            CommentSerializer(comment, context = {'request': request}).data,
            status=status.HTTP_200_OK,
        )
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        # DRF default destroy return status code = 204 no content
        # but here we return sucess=True, can make judgement more straight forward
        # so return 200 is better
        return Response({'success': True}, status = status.HTTP_200_OK)
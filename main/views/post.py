from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from main.serializers import PostSerializer,Post

@extend_schema(tags=['Post'])
class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticated,]


    

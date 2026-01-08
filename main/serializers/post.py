from rest_framework import serializers
from main.models import User,Post,PostMedia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','phone']
  


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user','content','liked_users','viewed_users',]
        read_only_fields = ['id','liked_users','viewed_users','created_at','updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['user'] = UserSerializer(instance.user).data
        # data['media'] = MediaSerializer(instance.medias).data
        data['liked_users'] = UserSerializer(instance.liked_users,many=True).data
        data['viewed_users'] = UserSerializer(instance.liked_users,many=True).data

        return data
   

    
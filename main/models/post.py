from django.db import models



class Post(models.Model):
    user = models.ForeignKey("main.User",on_delete=models.CASCADE,related_name='user')
    content = models.TextField()
    liked_users = models.ManyToManyField("main.User",related_name='liked_posts')
    viewed_users = models.ManyToManyField("main.User",related_name='viewed_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.username
    

class PostMedia(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='medias')
    media = models.FileField(upload_to='post_media/',blank=True,null=True)

   
    

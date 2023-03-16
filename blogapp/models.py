from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics', default='default/pro_pic.png')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.CharField(max_length=120, null=True, blank=True)

    mobile = models.CharField(max_length=12, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, null=True, blank=True)
    following = models.ManyToManyField(User, related_name='followings', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    @property
    def get_following(self):
        return self.following.all()

    @property
    def get_following_count(self):
        return self.get_following.count()

    @property
    def get_followers(self):
        return self.followers.all()

    @property
    def get_followers_count(self):
        return self.get_followers.count()

    @property
    def get_suggestions(self):
        all_user_profiles = UserProfile.objects.all().exclude(user=self.user)
        all_user_list = [userprofile.user for userprofile in all_user_profiles]
        following_list = [user for user in self.get_following]
        invitations = [user for user in all_user_list if user not in following_list]
        return invitations

    def __str__(self):
        return self.get_suggestions[:3]



    def __str__(self):
        return self.user.username


class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blog')

    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User)

    class Meta:
        ordering = ['-updated_at']

    @property
    def get_liked_users(self):
        return self.liked_by.all()

    @property
    def get_likes_count(self):
        return self.get_liked_users.count()

    def __str__(self):
        return self.description[:10]

    def __str__(self):
        return self.user.username

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='blog_comment')
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.comment

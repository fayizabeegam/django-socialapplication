from django.contrib import admin
from blogapp.models import Blogs, Comments, User, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Blogs)
admin.site.register(Comments)


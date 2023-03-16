from _ast import Pass

from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView,TemplateView
from django.views import View
from blogapp.models import User, Blogs, Comments, UserProfile
from blogapp.forms import (BlogsForm, CommentForm, UserRegistrationForm,
                           LoginForm, ProfileForm, ProfilePicForm)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# ======= home page view =========
@method_decorator(login_required(login_url='signin'), name='dispatch')
class HomeView(CreateView):
    model = Blogs
    form_class = BlogsForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blogs.objects.all().order_by('-updated_at')
        context['blogs'] = blogs
        comment_form = CommentForm()
        context['comment_form'] = comment_form

        return context


# =========== blog edit ===========
@method_decorator(login_required(login_url='signin'), name='dispatch')
class BlogEditView(View):

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('id')
        blog = Blogs.objects.get(id=blog_id)
        context = {
            'form': BlogsForm(instance=blog)
        }

        return render(request, 'blog_edit.html', context)

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('id')
        blog = Blogs.objects.get(id=blog_id)
        form = BlogsForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')


# ========== blog delete ==========
@login_required(login_url='signin')
def blogDeleteView(request, *args, **kwargs):
    blog_id = kwargs.get('id')
    blog = Blogs.objects.get(id=blog_id)
    blog.delete()
    return redirect('home')


@login_required(login_url='signin')
def searchBlogView(request):
    search_input = request.GET.get('search-input')
    blogs = Blogs.objects.filter(
        Q(title__icontains=search_input) |
        Q(description__icontains=search_input) |
        Q(user__username__icontains=search_input)).order_by('-updated_at')
    return render(request, 'search.html', {'blogs': blogs})


# ========== blog filter ===========
@login_required(login_url='signin')
def filterByLanguageView(request, *args, **kwargs):
    language = kwargs.get('slug')
    blogs = Blogs.objects.filter(related_language__iexact=language)
    context = {
        'blogs': blogs,
        'comment_form': CommentForm(),
        'no_blog_post': True
    }
    return render(request, 'home.html', context)


# =========== add comment ===========
@login_required(login_url='signin')
def addcommentView(request, *args, **kwargs):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = Blogs.objects.get(id=blog_id)
        user = request.user
        comment = request.POST.get('comment')
        Comments.objects.create(
            blog=blog,
            user=user,
            comment=comment)
        return JsonResponse({'suucess': 'comment added'})


# ========== edit comment ==========
@method_decorator(login_required(login_url='signin'), name='dispatch')
class CommentEditView(View):
    comment = None

    def get(self, request):
        comment_id = request.GET.get('comment_id')
        global comment
        comment = Comments.objects.get(id=comment_id)
        data = {
            'comment': comment.comment
        }
        print(data)
        return JsonResponse(data)

    def post(self, request):
        instance = comment
        comment_input = request.POST.get('comment')
        instance.comment = comment_input
        instance.save()
        return JsonResponse({'suucess': 'comment edited'})


# ========= delete comment ===========
@login_required(login_url='signin')
def deletecommentView(request, *args, **kwargs):
    comment_id = request.GET.get('comment_id')
    comment = Comments.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'suucess': 'comment deleted'})


# ============ like blog ============
@login_required(login_url='signin')
def likeView(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = Blogs.objects.get(id=blog_id)
        blog.liked_by.add(request.user)
        return JsonResponse({'suucess': 'liked'})


# ========== unlike blog ===========
@login_required(login_url='signin')
def unlikeView(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = Blogs.objects.get(id=blog_id)
        blog.liked_by.remove(request.user)
        return JsonResponse({'suucess': 'unliked'})


# ========= remove followers ===========
@login_required(login_url='signin')
def removeFollowerView(request):
    if request.method == 'POST':
        follower_user_id = request.POST.get('follower_user_id')
        follower_user = User.objects.get(id=follower_user_id)
        follower_user_profile = UserProfile.objects.get(user=follower_user)
        follower_user_profile.following.remove(request.user)
        follower_user_profile.save()

        remove_request_user_profile = request.user.user_profile
        remove_request_user_profile.followers.remove(follower_user)
        remove_request_user_profile.save()

        return JsonResponse({'suucess': 'followed'})


# ========= follow users ========
@login_required(login_url='signin')
def followView(request):
    if request.method == 'POST':
        follow_user_id = request.POST.get('follow_user_id')
        follow_user = User.objects.get(id=follow_user_id)
        follow_user_profile = UserProfile.objects.get(user=follow_user)
        follow_user_profile.followers.add(request.user)
        follow_user_profile.save()

        follow_request_user_profile = request.user.user_profile
        follow_request_user_profile.following.add(follow_user)
        follow_request_user_profile.save()

        return JsonResponse({'suucess': 'followed'})

#================ connections==================#
@method_decorator(login_required(login_url='signin'), name='dispatch')

class ConnectionsView(TemplateView):
    template_name = 'connections.html'


# ======== unfollow users =========
@login_required(login_url='signin')
def unfollowView(request):
    if request.method == 'POST':
        following_user_id = request.POST.get('following_user_id')
        following_user = User.objects.get(id=following_user_id)
        following_user_profile = UserProfile.objects.get(user=following_user)
        following_user_profile.followers.remove(request.user)
        following_user_profile.save()

        unfollow_request_user_profile = request.user.user_profile
        unfollow_request_user_profile.following.remove(following_user)
        unfollow_request_user_profile.save()

        return JsonResponse({'suucess': 'followed'})


# ======= user registration =========
class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    model = User
    success_url = reverse_lazy('signin')


# =========user login ==========
class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    model=User

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            p_word=form.cleaned_data.get("password")
            user=authenticate(request,username=user_name,password=p_word)
            if user:
                print("success")
                login(request,user)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":self.form_class})


# ========= user logout ============
@login_required(login_url='signin')
def signoutView(request, *args, **kwargs):
    logout(request)
    return redirect('signin')


# ========= user profile ============
@method_decorator(login_required(login_url='signin'), name='dispatch')
class MyProfileView(View):

    def get(self, request):
        return render(request, 'my_profile.html')

    def post(self, request):
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect('my-profile')


# ========== user profile add view =========
@method_decorator(login_required(login_url='signin'), name='dispatch')
class ProfileAddView(CreateView):
    form_class = ProfileForm
    template_name = 'profile_add.html'
    model = UserProfile
    success_url = reverse_lazy('my-profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


# ========== user profile edit =========
@method_decorator(login_required(login_url='signin'), name='dispatch')
class ProfileEditView(View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'profile_add.html', {'form': form})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'my_profile.html')


# ======= other user profile ==========
@login_required(login_url='signin')
def otherProfileView(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = User.objects.get(id=user_id)
    return render(request, 'other-profile.html', {'user': user})


# connections

from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import LikeForm, CommentForm
from .models import Like, Comment
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(date__lte=timezone.now()).order_by('-date')

    for post in posts:
        likes = Like.objects.select_related('post').filter(post=post.id).count()
        comments = Comment.objects.select_related('post').filter(post=post.id).count()

        post.likes = likes
        post.comments = comments


    return render(request, 'blog/post_list.html', {'posts': posts})

def single_post(request):
    id = request.GET.get('id','None')

    if id != 'None':
        post = Post.objects.get(id=id)

        likes = Like.objects.select_related('post').filter(post=post.id).count()
        comment_num = Comment.objects.select_related('post').filter(post=post.id).count()

        likes = Like.objects.select_related('post').filter(post=post.id).count()
        comments = Comment.objects.select_related('post').filter(post=post.id).count()

        post.likes = likes
        post.comments = comment_num

        comments = Comment.objects.select_related('post').filter(post=post.id)

        return render(request, 'blog/single_post.html', {'post': post, 'comments': comments})
    else:
        return HttpResponseRedirect('/')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def store_like(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)

        try:
            like = Like.objects.get(user=request.POST['user'],post=request.POST['post'])
            like.delete()
        except ObjectDoesNotExist:
            form.save()
        except ValueError:
            messages.add_message(request, messages.ERROR, 'You cannot like a post if you are not signed in.')
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

def store_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        form.date = datetime.datetime.now()

        try:
            form.save()
        except ValueError:
            messages.add_message(request, messages.ERROR, 'You cannot add a comment if you are not signed in.')

    return HttpResponseRedirect('/')

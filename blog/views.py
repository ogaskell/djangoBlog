from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import LikeForm
from .models import Like

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(date__lte=timezone.now()).order_by('-date')



    for post in posts:
        likes = Like.objects.select_related('post').filter(post=post.id).count()
        post.likes = likes


    return render(request, 'blog/post_list.html', {'posts': posts})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def store_like(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        from django.core.exceptions import ObjectDoesNotExist
        try:
            like = Like.objects.get(user=request.POST['user'],post=request.POST['post'])
            like.delete()
        except ObjectDoesNotExist:
            form.save()

    return HttpResponseRedirect('/')

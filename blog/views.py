from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.models import User, Group
from .models import Post
from .forms import PostForm

from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, PostSerializer

# Create your views here.
def post_list(request):
    posts = Post.objects\
        .filter(published_date__lte=timezone.now())\
        .order_by('published_date')

    return render(request, 'blog/post_list.html',
                  {'posts':posts})
#
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
#
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    #
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


#
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

#
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#
class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
#
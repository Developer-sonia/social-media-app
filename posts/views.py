from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post
from django.contrib.auth.models import User

def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Default: Show latest posts first

    # Filtering by date
    date_filter = request.GET.get('date_filter')
    if date_filter == 'oldest':
        posts = posts.order_by('created_at')

    # Filtering by media type
    media_filter = request.GET.get('media_filter')
    if media_filter == 'text':
        posts = posts.filter(image__isnull=True)
    elif media_filter == 'images':
        posts = posts.filter(image__isnull=False)

    # Filtering by user
    user_filter = request.GET.get('user_filter')
    if user_filter:
        posts = posts.filter(author__username=user_filter)

    # Searching by keyword
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(Q(content__icontains=search_query))

    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    # Filtering by date
    date_filter = request.GET.get('date_filter')
    if date_filter == 'oldest':
        posts = posts.order_by('created_at')

    # Filtering by media type
    media_filter = request.GET.get('media_filter')
    if media_filter == 'text':
        posts = posts.filter(image__isnull=True)
    elif media_filter == 'images':
        posts = posts.filter(image__isnull=False)

    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)
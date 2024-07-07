from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import PostForm
from .models import Post


@require_http_methods(["GET", "POST", "OPTIONS"])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return JsonResponse({'error': form.errors}, status=400)

@require_http_methods(["GET", "OPTIONS"])
def post_detail(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

@require_http_methods(["GET", "POST", "OPTIONS"])
@login_required
def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return JsonResponse({'error': form.errors}, status=400)

@require_http_methods(["GET", "POST", "OPTIONS"])
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return JsonResponse({'error': form.errors}, status=400)

@require_http_methods(["GET", "POST", "OPTIONS"])
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        return render(request, 'blog/post_delete.html', {'post': post})
    elif request.method == 'POST':
        post.delete()
        return redirect('post_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/registration/login.html', {'form': form})
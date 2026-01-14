from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# the last import should be removed if not used

from .models import Blog, Comment

def index(request):
	blogs = Blog.objects.all().order_by('-created_at')
	return render(request, 'index.html', {'blogs': blogs})

def search(request):
	query = request.GET.get('q', '')
	"""
	blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by('-created_at')
	"""

	with connection.cursor() as cursor:
		sql = f"""
            SELECT b.id, b.title, b.content, u.username FROM blogs_blog b JOIN auth_user u ON b.author_id = u.id 
            WHERE b.title LIKE '%{query}%' OR b.content LIKE '%{query}%' ORDER BY b.created_at DESC
        """
		cursor.execute(sql)
		blogs = cursor.fetchall()
	blogs = [{'id': b[0], 'title': b[1], 'author': {'username': b[2]}} for b in blogs]

	return render(request, 'index.html', {'blogs': blogs, 'query': query})

def blog_detail(request, blog_id):
	blog = get_object_or_404(Blog, id=blog_id)
	comments = Comment.objects.filter(blog=blog)
	if request.method == 'POST':
		content = request.POST.get('content')
		if content:
			Comment.objects.create(blog=blog, author=request.user, content=content)
	return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments})

@login_required
def blog_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		if title and content:
			Blog.objects.create(title=title, content=content, author=request.user)
			return redirect('index')
	return render(request, 'blog_form.html')

@login_required
def blog_delete(request, blog_id):
	blog = get_object_or_404(Blog, id=blog_id)
	if request.user != blog.author:
		return redirect('blog_detail', blog_id=blog_id)
	if request.method == 'POST':
		blog.delete()
		return redirect('index')
	return render(request, 'index.html')

#@login_required
def comment_delete(request, blog_id, comment_id):
	comment = get_object_or_404(Comment, id=comment_id, blog_id=blog_id)
	#if request.user != comment.author:
	#	return redirect('blog_detail', blog_id=blog_id)
	if request.method == 'POST':
		comment.delete()
	return redirect('blog_detail', blog_id=blog_id)

def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			user = User.objects.create_user(username=username, password=password)
			login(request, user)
			return redirect('index')
	return render(request, 'register.html')

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('index')
		else:
			return render(request, 'login.html', {'error': 'Invalid credentials'})
	return render(request, 'login.html')

def logout_view(request):
	logout(request)
	return redirect('index')

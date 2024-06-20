from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Blog, Category, Comment
from .forms import CommentForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

def index(request):
    blogs = Blog.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        "blogs": blogs,
        "categories": categories
    }
    return render(request, "blog/index.html", context)

def blogs(request):
    blogs = Blog.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        "blogs": blogs,
        "categories": categories
    }
    return render(request, "blog/blogs.html", context)

def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()
    context = {
        "blog": blog,
        "comments": comments,
        "form": form
    }
    return render(request, "blog/blog-details.html", context)

def blogs_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blogs = category.blog_set.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        "blogs": blogs,
        "categories": categories,
        "selected_category": category
    }
    return render(request, "blog/blogs.html", context)

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        return redirect('blog_details', slug=comment.blog.slug)
    return HttpResponse("Bu yorumu silme izniniz yok veya bu sayfaya doğrudan erişim izniniz yok.")

def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        if 'btn_comment_edit' in request.POST:
            return redirect('blog_details', slug=comment.blog.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_edit.html', {'form': form})

@login_required(login_url="index")
def profile(request, user_id):
    current_user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(is_active=True)
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'btnChangePassword' in request.POST:
            current_password = request.POST.get('current_password').strip()
            new_password = request.POST.get('new_password').strip()
            check_password = request.POST.get('check_password').strip()

            if current_user.check_password(current_password):
                if new_password == check_password:
                    current_user.set_password(new_password)
                    current_user.save()
                    user = authenticate(request, username=current_user.username, password=new_password)
                    auth.login(request, user)
                    return render(request, 'blog/profile.html', {"blogs": blogs, "categories": categories, 'user': current_user, 'PWChanged': True})
                else:
                    return render(request, 'blog/profile.html', {"blogs": blogs, "categories": categories, 'user': current_user, 'PWnotMatched': True})
            else:
                return render(request, 'blog/profile.html', {"blogs": blogs, "categories": categories, 'user': current_user, 'PWisWrong': True})

        elif 'btnChangeMail' in request.POST:
            mail = request.POST.get('mail').strip()
            current_mail = current_user.email
            if current_mail == mail:
                return render(request, 'blog/profile.html', {"blogs": blogs, "categories": categories, 'user': current_user, 'MailNotChanged': True})
            else:
                current_user.email = mail
                current_user.save()
                return render(request, 'blog/profile.html', {"blogs": blogs, "categories": categories, 'user': current_user, 'MailChanged': True})

    context = {
        "blogs": blogs,
        "categories": categories,
        'user': current_user,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user == user or request.user.is_superuser:
        user.delete()
        return redirect('home')
    else:
        return HttpResponseForbidden("Bu işlemi gerçekleştirme yetkiniz yok.")

class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected_template.html'


def about(request):
    return render(request, 'blog/about.html')

    
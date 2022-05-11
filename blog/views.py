from re import template
from unicodedata import category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views import View
from .models import Blog, Category, Tag
from .forms import BlogForm, CommentForm, BlogUpdateForm
from django.views.generic import DeleteView, ListView
from user.models import UserProfile
from django.db.models import Q

class BasicView:
    def category(request):
        categories = Category.objects.all()
        return categories
    
    def tag(request):
        tags = Tag.objects.all()
        return tags


class Home(BasicView, View):
    def get(self, request):
        context = {}
        search_title = request.GET.get('search')
        if search_title:
            context['blogs'] = Blog.objects.filter(
                Q(title__icontains=search_title) | Q(category__name__icontains=search_title))
        else:
            context['blogs'] = Blog.objects.all()
                    
        context['categories'] = self.category()
        context['tags'] = self.tag()
        
        return render(request, 'home.html', context)


class CategoryBlog(BasicView, View):
    def get(self, request, slug):
        context = {}
        category = Category.objects.get(slug=slug)
        context['category'] = category
        context['blogs'] = Blog.objects.filter(category=category)
        context['categories'] = self.category()
        context['tags'] = self.tag()       
        
        return render(request, 'category_or_tag_blogs.html', context)
    
    
class TagBlog(BasicView, View):
    def get(self, request, slug):
        context = {}
        tag = Tag.objects.get(slug=slug)
        context['tag'] = tag
        context['blogs'] = Blog.objects.filter(tags=tag)
        context['categories'] = self.category()
        context['tags'] = self.tag()

        return render(request, 'category_or_tag_blogs.html', context)


class BlogCreate(LoginRequiredMixin,BasicView, View):
    login_url = reverse_lazy('login')
    def get(self, request):
        context = {}
        context['categories'] = self.category()
        context['tags'] = self.tag() 
        context['form'] = BlogForm()
        return render(request, 'blog_create.html', context)
    
    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form_create = form.save(commit=False)
            form_create.slug = slugify(form_create.title)
            form_create.user = request.user
            form_create.save()
            blog = Blog.objects.get(id=form_create.id)
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag.strip())
                blog.tags.add(tag)
            return redirect('home')
        


class BlogDetail(BasicView, View):
    def get(self, request, slug):
        context = {}
        blog = Blog.objects.get(slug=slug)
        context['blog'] = blog
        context['categories'] = self.category()
        context['tags'] = self.tag()
        context['form'] = CommentForm()
        
        blog.views += 1
        blog.save()

        return render(request, 'blog_detail.html', context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        blog = Blog.objects.get(slug=slug)
        if form.is_valid():
            form_comment = form.save(commit=False)
            form_comment.blog = blog
            form_comment.user = request.user
            form_comment.save()
            return redirect('blog', blog.slug)
        
    
        
        
class BlogUpdate(View):
    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        str1 = ''
        for tag in blog.tags.all():
            str1 += str(tag)
            str1 += ','
        
        context = {}
        context['form'] = BlogUpdate(instance=blog)
        context['str1'] = str1
       
        return render(request, 'blog_update.html', context)
    
    def post(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        form = BlogUpdateForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form_create = form.save(commit=False)
            form_create.slug = slugify(form_create.title)
            form_create.user = request.user
            form_create.save()
            blog = Blog.objects.get(id=form_create.id)
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                if tag!='':
                    tag, created = Tag.objects.get_or_create(name=tag.strip())
                    blog.tags.add(tag)
            return redirect('blog', blog.slug)
        
        
class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('home') 
    template_name = 'blog_delete.html'   
    

class CategoryList(ListView, BasicView):
    model = Category
    context_object_name = 'category_list'
    template_name = 'category_list.html'
    
    def get_context_data(self,*, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.category()
        context['tags'] = self.tag()
        
        return context
    

class CategoryAddUser(View):
    def get(self, request, slug):
        user = UserProfile.objects.get(username=request.user.username)
        category = Category.objects.get(slug=slug)
        if category.user.filter(username=request.user.username).exists():
            category.user.remove(user)
            return redirect('category_list')
        else:
            category.user.add(user)
            return redirect('category_list')
        
class UserList(View):
    
    def get(self, request):
        user_search = request.GET.get('search')
        if user_search:
            list_user = UserProfile.objects.filter(username__icontains=user_search)
        
        else:
            list_user = UserProfile.objects.all()
            
        context = {
            'users':list_user
        }
        
        return render(request, 'list_user.html', context)
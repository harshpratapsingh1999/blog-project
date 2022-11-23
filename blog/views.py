from math import fabs
from multiprocessing import context
from tkinter.messagebox import NO
from xml.etree.ElementInclude import include
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# def starting_page(request):
    # latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

class StagingView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        base_query =  super().get_queryset()
        data = base_query[:3]    
        return data


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "posts": all_posts
#     })

class AllPostView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "posts"





# def post_details(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         "post": post,
#         "tags": post.tags.all()
#     })


class DetailedPostView(View):
    
    def get(self, request, slug):
        post = Post.objects.get(slug = slug)
        comment_form = CommentForm()
        stored_posts = request.session.get("stored_post")
        added_to_read_later = False
        
        if stored_posts is not None and post.id in stored_posts:
            added_to_read_later = True
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": comment_form,
            "all_comments": Comment.objects.all().order_by("-id"),
            "added_to_read_later": added_to_read_later
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
            post = Post.objects.get(slug = slug)
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

            context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": comment_form 
            }
            return render(request, "blog/post-detail.html", context)         


    
class ReadLaterView(View):
    
    def get(self, request):
        stored_post = request.session.get("stored_post")
        context = {}
        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
           posts = Post.objects.filter(id__in = stored_post)
           context["posts"] = posts
           context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)    


    def post(self, request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST['post_id'])

        if post_id not in stored_post:
            stored_post.append(post_id)
            
        else:
            stored_post.remove(post_id)    
        request.session['stored_post'] = stored_post
        return HttpResponseRedirect("/blog/")    



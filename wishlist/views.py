from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import UpdateView, CreateView, DetailView, ListView

from wishlist.forms import PostForm
from wishlist.models import Post, Tag
from wishlist.widgets import StarWidget


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [ 'link', 'price', 'memo', 'need', 'want', 'tags']
    template_name = "wishlist/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [ 'link', 'price', 'memo', 'need', 'want', 'tags']
    # form_class = PostForm

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else :
            return redirect('/wishlist')

class PostList(LoginRequiredMixin, ListView):
    model = Post
    # ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['tags'] = Tag.objects.filter(author=self.request.user)
        context['post_list'] = Post.objects.filter(author=self.request.user).order_by('-pk')

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()

        return context

def purchase_change(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.purchase = not post.purchase
    post.save()
    return redirect('/wishlist')

def show_purchase_list(request):
    post_list = Post.objects.filter(author = request.user, purchase = True).order_by('-pk')

    context = {
        'post_list' : post_list
    }
    return render(request, 'wishlist/purchase_list.html', context)

def show_tag_posts(request, slug):

    tag = Tag.objects.get(slug = slug)
    post_list = tag.post_set.all().order_by('-pk')
    tags = Tag.objects.filter(author = request.user)

    context = {
        'tag' : tag,
        'post_list' : post_list,
        'tags' : tags
    }

    return render(request, 'wishlist/post_list.html', context)



import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, ListView, FormView, DeleteView

from wishlist.forms import PostForm, PostByLinkForm, TagForm
from wishlist.models import Post, Tag
from wishlist.widgets import StarWidget
from django.utils.text import slugify


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    # fields = [ 'link', 'price', 'memo', 'need', 'want', 'tags']
    form_class = PostByLinkForm
    template_name = "wishlist/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

class PostCreate(LoginRequiredMixin, CreateView):
    # model = Post
    # fields = [ 'link', 'price', 'memo', 'need', 'want', 'tags']
    form_class = PostByLinkForm
    template_name = 'wishlist/post_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['tags'] = Tag.objects.filter(author=self.request.user)

        return context

    def form_valid(self, form):
        current_user = self.request.user

        post = form.save(commit=False)
        url_receive = post.link

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        print(soup.select_one('meta[property="og:title"]')['content'])
        post.title = soup.select_one('meta[property="og:title"]')['content']
        post.head_image = soup.select_one('meta[property="og:image"]')['content']
        post.save()

        selected = self.request.POST.getlist('selected')
        # print(selected)
        for i in selected:
            post.tags.add(i)

        post.save()

        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else :
            return redirect('/wishlist')


class PostDelete(DeleteView):
    model = Post
    success_url = '/wishlist'


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

class TagCreate(LoginRequiredMixin, CreateView):
    form_class = TagForm
    template_name = 'wishlist/tag_form.html'

    def form_valid(self, form):
        current_user = self.request.user

        tag = form.save(commit=False)
        tag.author = current_user
        tag.save()

        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(TagCreate, self).form_valid(form)
        else :
            return redirect('/wishlist')



# def sort_post(request):
#     sort = request.GET.get('sort', '')
#
#     if sort == 'need':
#         posts = Post.objects.order_by('-need', '-pk')
#         return render(request, 'wishlist/post_list.html', {'post_list': posts})
#     # elif sort == 'want':
#     #     user = request.user
#     #     memos = Memos.objects.filter(name_id=user).order_by('-update_date')  # 복수를 가져올수 있음
#     #     return render(request, 'memo_app/index.html', {'memos': memos})
#     # else:
#     #     posts = Post.objects.filter(author = request.user).order_by('-pk')
#     #     return render(request, 'memo_app/index.html', {'memos': memos})
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime

from django.views.generic import ListView, DetailView, DeleteView, CreateView

from .filters import PostFilter
from .models import Post
from django.urls import reverse_lazy


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts_list')


class PostCreate(CreateView):
    model = Post
    template_name = 'create.html'
    context_object_name = 'post_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/article/create':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)


class PostEdit(ListView):
    model = Post
    template_name = 'edit.html'
    context_object_name = 'post_edit'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
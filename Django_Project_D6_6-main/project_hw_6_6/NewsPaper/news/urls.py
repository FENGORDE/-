from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostDelete, PostEdit, PostSearch

urlpatterns = [
    # path('', PostList.as_view(), name='post_list'),
    path('', PostList.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post_create/', PostCreate.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('article/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]

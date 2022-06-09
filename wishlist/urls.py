from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/delete', views.PostDelete.as_view()),
    path('tag/<str:slug>/', views.show_tag_posts),
    path('add_tag/', views.TagCreate.as_view()),
    path('purchase_change/<int:pk>', views.purchase_change),
    path('purchased_item/', views.show_purchase_list)
]
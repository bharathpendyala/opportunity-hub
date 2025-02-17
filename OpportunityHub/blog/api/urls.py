from django.urls import path

from OpportunityHub.blog.views import BlogPostListCreateAPIView, BlogPostRetrieveUpdateDestroyAPIView, CommentListCreateAPIView, \
    CommentRetrieveUpdateDestroyAPIView, LatestBlogPostsAPIView

urlpatterns = [
    path('blog/<int:pk>/', BlogPostRetrieveUpdateDestroyAPIView.as_view(), name='blog-detail'),
    path('blog/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('blog/<int:pk>/comments/<int:comment_pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('blog/last/', LatestBlogPostsAPIView.as_view(), name='last-5-blogs'),
]


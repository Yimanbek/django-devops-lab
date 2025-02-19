from .views import PostAdminDetailViews, PostAdminViews, PostListViews
from django.urls import path

urlpatterns = [
    path('list/', PostListViews.as_view()),
    path('', PostAdminViews.as_view()),
    path('<int:pk>/', PostAdminDetailViews.as_view())
]
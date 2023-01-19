from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter


from . import views

status_router = DefaultRouter()
status_router.register('status', views.StatusViewSet)

urlpatterns = [
    path('news/', views.NewsListCreateApiView.as_view()),
    path('news/<int:news_id>/', views.NewsRetrieveUpdateDestroyApiView.as_view()),

    path('news/<int:news_id>/comment/', views.CommentsListCreateApiView.as_view()),
    path('news/<int:news_id>/comment/<int:pk>/', views.CommentRetrieveUpdateDestroyApiView.as_view()),

    path('', include(status_router.urls)),

    path('news/<int:news_id>/<str:slug>/',views.NewsStatusApiView.as_view()),
    path('news/<int:news_id>/comment/<int:comment_id>/<str:slug>/',views.CommentStatusApiView.as_view()),
]
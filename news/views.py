from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication,TokenAuthentication

from rest_framework.filters import OrderingFilter,SearchFilter

from .models import News,Comment,NewsStatus,CommentStatus,Status
from .serializers import NewsSerializer,CommentSerializer,StatusSerializer
from .permissions import IsAuthorOrReadOnly,IsOwnerOrReadOnly
from .paginations import NewsCommentPagination

class NewsListCreateApiView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('pk')
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly,]
    pagination_class = NewsCommentPagination
    filter_backends = [OrderingFilter,SearchFilter]
    ordering_fields = ['created',]
    search_fields = ['title',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

class NewsRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly,]

    def get_object(self):
        return super().get_queryset().filter(pk=self.kwargs.get('news_id',None)).first()

class CommentsListCreateApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly,]
    pagination_class = NewsCommentPagination

    def get_queryset(self):
        news_obj = News.objects.filter(pk=self.kwargs.get('news_id', None)).first()
        return Comment.objects.filter(news=news_obj).order_by('pk')

    def perform_create(self, serializer):
        news_obj = News.objects.filter(pk=self.kwargs.get('news_id',None)).first()
        return serializer.save(news=news_obj,author=self.request.user.author)

class CommentRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly,]

    def get_queryset(self):
        news_obj = News.objects.filter(pk=self.kwargs.get('news_id', None)).first()
        return Comment.objects.filter(news=news_obj)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser,]

class NewsStatusApiView(APIView):
    permission_classes = [IsAuthorOrReadOnly,]

    def get(self,request,*args,**kwargs):
        news_obj = News.objects.filter(pk=self.kwargs.get('news_id', None)).first()
        status_obj = Status.objects.filter(slug=kwargs.get('slug',None)).first()
        try:
            status_news = NewsStatus(news=news_obj,status=status_obj,author=request.user.author)
            status_news.save()
            context = {'message': 'Status added'}
            return Response(context)
        except IntegrityError:
            context = {'error': 'You already added status'}
            return Response(context)

class CommentStatusApiView(APIView):
    permission_classes = [IsAuthorOrReadOnly,]

    def get(self,request,*args,**kwargs):
        news_obj = News.objects.filter(pk=kwargs.get('news_id')).first()
        status_obj = Status.objects.filter(slug=kwargs.get('slug')).first()
        comment_obj = Comment.objects.filter(pk=kwargs.get('comment_id'),news=news_obj).first()
        try:
            status_news = CommentStatus(comment=comment_obj,status=status_obj,author=request.user.author)
            status_news.save()
            context = {'message': 'Status added'}
            return Response(context)
        except IntegrityError:
            context = {'error': 'You already added status'}
            return Response(context)









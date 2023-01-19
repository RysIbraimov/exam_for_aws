from rest_framework import serializers

from .models import News,Comment,Status

class NewsSerializer(serializers.ModelSerializer):
    status_count = serializers.ReadOnlyField(source='news_status_count')
    class Meta:
        model = News
        fields = ['title','content','status_count']
        read_ony_fields = ['author',]

class CommentSerializer(serializers.ModelSerializer):
    status_count = serializers.ReadOnlyField(source='comment_status_count')
    class Meta:
        model = Comment
        fields = ['text','status_count']
        read_ony_fields = ['author','news']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

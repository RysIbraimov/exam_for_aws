from django.db import models
from django.db.models import Count
from account.models import Author

class PostAbstract(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_status(self, statuses):
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']

        return result

class News(PostAbstract):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    def news_status_count(self):
        statuses = NewsStatus.objects.filter(news=self).values('status__name').annotate(count=Count('status'))
        return self.get_status(statuses)

class Comment(PostAbstract):
    text = models.CharField(max_length=255)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment : {self.news}'

    def comment_status_count(self):
        statuses = CommentStatus.objects.filter(comment=self).values('status__name').annotate(count=Count('status'))
        return self.get_status(statuses)

class Status(models.Model):
    slug = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class StatusAbstract(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class NewsStatus(StatusAbstract):
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['news','author']

    def __str__(self):
        return f'Status for news : {self.news}'

class CommentStatus(StatusAbstract):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['comment','author']

    def __str__(self):
        return f'Status for comment :  {self.comment}'

    def __str__(self):
        return f'New status to  {self.comment}'


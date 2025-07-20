from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=30, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self):
        post_rating = sum(post.rating_news*3 for post in self.post_set.all())
        user_comment_rating = sum(comment.rating_comment for comment in Comment.objects.filter(user=self.user))
        post_comment_rating = sum(
            comment.rating_comment
            for post in self.post_set.all()
            for comment in Comment.objects.filter(post=post)
        )
        self.rating = post_rating + user_comment_rating + post_comment_rating
        self.save()

class Category (models.Model):
    name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, through='UsersCategory')

    def __str__(self):
        return self.name

class UsersCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    news = 'nw'
    article='st'
    NEWS = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    type = models.CharField(max_length=2,
                              choices=NEWS,
                              default=article)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category,
                                         through='PostCategory')
    title = models.CharField(max_length=255)
    text_news = models.TextField()
    rating_news = models.IntegerField(default=0)

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return f'{self.text_news[:124]}...'

    def __str__(self):
        return f'{self.title}: {self.text_news}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

from django.db import models


from NewsPortal.account.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

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


class Post(models.Model):
    news = 'nw'
    article='st'
    NEWS = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    choice = models.CharField(max_length=2,
                              choices=NEWS,
                              default=article)
    time_create = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category,
                                         through='PostCategory',
                                         through_fields=('category',
                                         'post'))
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


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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

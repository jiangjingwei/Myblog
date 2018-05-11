from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(AbstractUser):
    """ 用户信息 """
    SEX_CHOICES = (
        (0, '女'),
        (1, '男')
    )

    nickname = models.CharField(max_length=32, verbose_name='用户昵称')
    sex = models.CharField(max_length=5, choices=SEX_CHOICES, null=True, blank=True)
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    avatar = models.FileField(upload_to='./upload/img/', default='./upload/img/default.png', verbose_name='头像')
    blog = models.OneToOneField('Blog', null=True)
    register_time = models.DateField(auto_now_add=True, verbose_name='注册时间')


class Blog(models.Model):
    """ 个人站点 """

    site = models.CharField(max_length=32, verbose_name='个人博客站点前缀')
    title = models.CharField(max_length=32, verbose_name='个人博客标题')
    theme = models.CharField(max_length=32, verbose_name='博客主题')


class Article(models.Model):
    """ 文章 """

    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=200, verbose_name='文章描述')
    detail = models.OneToOneField('ArticleDetail', verbose_name='文章内容')
    user = models.ForeignKey('UserInfo', verbose_name='作者')
    create_date = models.DateField(auto_now_add=True, verbose_name='创建时间')

    comment_num = models.IntegerField(default=0, verbose_name='评论数')
    vote_num = models.IntegerField(default=0, verbose_name='点赞数')
    views_num = models.IntegerField(default=0, verbose_name='阅读数')

    category = models.ForeignKey('Category', null=True, verbose_name='分类')
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=['article', 'tags'])


class ArticleDetail(models.Model):
    """ 文章内容 """
    content = models.TextField()


class Category(models.Model):
    """ 分类 """
    name = models.CharField(max_length=32, verbose_name='分类名称')
    blog = models.ForeignKey('Blog', verbose_name='所属博客')


class Article2Tag(models.Model):
    """ 文章与标签关系表 """
    article = models.ForeignKey('Article')
    tags = models.ForeignKey('Tag')

    class Meta:
        unique_together = ['article', 'tags']


class Tag(models.Model):
    """ 标签 """
    name = models.CharField(max_length=32, verbose_name='标签名称')
    blog = models.ForeignKey('Blog', verbose_name='所属博客')


class Comment(models.Model):
    """ 评论 """
    article = models.ForeignKey('Article')
    user = models.ForeignKey('UserInfo', verbose_name='评论者')
    content = models.CharField(max_length=255, verbose_name='评论内容')
    create_time = models.DateField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, verbose_name='父评论')


class VoteUpDown(models.Model):
    """ 点赞和踩灭 """
    article = models.ForeignKey('Article')
    user = models.ForeignKey('UserInfo')
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = ['article', 'user']

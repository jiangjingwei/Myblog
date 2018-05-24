from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.forms import RegisterForm
from PIL import Image, ImageDraw, ImageFont
import random
import os
import json
import string
from io import BytesIO
from myblog import settings
from django.contrib import auth
from django.http import JsonResponse
from blog.models import UserInfo, Blog, Article, Category, Tag, VoteUpDown
from django.db.models import Count, F
from django.db import transaction
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def home_page(request, *args, **kwargs):

    user = UserInfo.objects.get(username='eric')
    if user:
        # 当前用户
        # user = UserInfo.objects.get(username=kwargs.get('username'))

        # 当前用户的blog
        current_blog = user.blog

        # 当前用户下所有的文章列表
        article_list = Article.objects.filter(user=user)

        # 文章分页
        paginator = Paginator(article_list, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        # print(paginator.num_pages)

        # 点击分类
        if kwargs.get('cate_pk'):
            category_id = kwargs.get('cate_pk')
            article_list = Article.objects.filter(user=user, category=category_id)

        # 点击标签
        if kwargs.get('tag_pk'):
            tag_id = kwargs.get('tag_pk')
            article_list = Article.objects.filter(user=user, tags=tag_id)

        # 当前blog下所有的分类和个数
        cate_list = Category.objects.filter(blog=current_blog).values_list('name', 'id').annotate(Count('name'))

        # 当前blog下所有的标签

        tags_list = Tag.objects.filter(blog=current_blog)

        return render(request, 'blog/index.html', locals())
    else:
        return redirect('/login/')


def article_detail(request, pk):
    # user = UserInfo.objects.get(username=request.user)

    # current_blog = user.blog

    # 阅读+1
    article = Article.objects.get(pk=pk)
    article.views_num += 1
    article.save()

    if request.is_ajax():
        comment_list = article.comment_set.values('user_id', 'content', 'parent_comment', 'create_time')
        comment_order_dic = OrderedDict()
        comment_dic = {}

        for item in comment_list:
            item['children_comment'] = []
            comment_dic[item['user_id']] = item

            if item['parent_comment']:
                comment_dic[item['parent_comment']]['children_comment'].append(item)
            else:
                comment_order_dic[item['user_id']] = comment_dic[item['user_id']]

        return JsonResponse(comment_order_dic)

    tag_list = Tag.objects.filter(article2tag__article=article)

    # 文章详情内容
    # content = article.detail.content

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)
    ])

    article.detail.content = md.convert(article.detail.content)
    article.detail.toc = md.toc

    return render(request, 'blog/articleDetail.html', locals())


def log_in(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = auth.authenticate(username=username, password=password)
        login_response = {'username': None, 'error': None}
        if user:
            auth.login(request, user)
            if json.loads(remember_me):
                request.session['username'] = user.username

            else:

                if request.session.get('username'):
                    del request.session['username']

            login_response['user'] = user.username
            return HttpResponse(json.dumps(login_response))

        else:
            login_response['error'] = '用户名密码错误'

            return HttpResponse(json.dumps(login_response))

    return render(request, 'blog/login.html')


def register(request):
    if request.is_ajax():
        form_obj = RegisterForm(request, request.POST)

        register_response = {'status': None, 'errors': None}
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')

            user = UserInfo.objects.create_user(username=username, password=password, email=email, telephone=phone)

            register_response['status'] = True

        else:
            print('验证失败', form_obj.errors)
            register_response['status'] = False
            register_response['errors'] = form_obj.errors

        return JsonResponse(register_response)

    register_form = RegisterForm(request)
    return render(request, 'blog/register.html', locals())


def get_captcha(request):
    img = Image.new('RGBA', (130, 44),
                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(img)

    for i in range(300):
        draw.point(
            (random.randint(0, 130), random.randint(0, 130)),
            fill=(0, 0, 0)
        )

        if i > 290:
            draw.line(
                [
                    (random.randint(0, 130), random.randint(0, 130)),
                    (random.randint(0, 130), random.randint(0, 130)),
                ],

                fill=(220, 220, 220)
            )

    font_file_path = os.path.join(settings.BASE_DIR, 'blog/static/dist/fonts/hakuyoxingshu7000.TTF')
    font = ImageFont.truetype(font_file_path, 24)

    captcha_code = random.sample(string.digits + string.ascii_letters, 5)
    captcha_img_code = " ".join(captcha_code)

    # 在session保存验证码
    request.session['captcha_code'] = ''.join(captcha_code)

    draw.text((12, 10), captcha_img_code, font=font,
              fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    f = BytesIO()
    img.save(f, 'png')

    return HttpResponse(f.getvalue())


def vote_up(request):
    if request.is_ajax():
        article_id = request.POST.get('article_id')
        user_id = request.POST.get('user_id')
        count = VoteUpDown.objects.filter(article_id=article_id, user_id=user_id).count()

        response = {
            'vote_status': None,
            'error_msg': None
        }

        if count:
            response['vote_status'] = 0
            response['error_msg'] = '已为此篇文章点赞'
        else:
            with transaction.atomic():
                VoteUpDown.objects.create(article_id=article_id, user_id=user_id, is_up=True)
                Article.objects.filter(id=article_id).update(vote_num=F('vote_num') + 1)
            response['vote_status'] = 1
            response['error_msg'] = '点赞成功'
        return JsonResponse(response)


def home_edit(request, user):
    print(request.session.get('username'))

    return render(request, 'blog/home_edit.html', locals())


def test(request):

    return render(request, 'blog/test.html')
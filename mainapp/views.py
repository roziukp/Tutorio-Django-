from django.shortcuts import render, redirect, reverse
from .forms import UserForm, ProfileForm, CVForm, CommentForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from . import models
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    return render(request, 'mainapp/index.html')


class Registr(View):
    template_name = 'mainapp/registration.html'
    form_class = UserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print('use1:', request.POST.get('use1'))
        if form.is_valid():
            form.save()
            newuser = auth.authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'], )
            if newuser is not None:
                auth.login(request, newuser)
                messages.success(request, 'User has been registered!')
            return redirect('/', {'message': messages})
        else:
            return render(request, self.template_name, {'form': form})


# дві функці на одному шаблоні поки що не працює
class Login(View):
    template_name = 'mainapp/index.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user=user)
            messages.success(request, 'User is logged!')
            return redirect('/')
        else:
            self.context['error']='Login error! Try again'
            return render(request, 'mainapp/index.html', self.context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@method_decorator(login_required, name='dispatch')
class GetProfileData(View):
    template_name = 'mainapp/profile_data.html'

    def get(self, request):
        try:
            profile_data = models.Profile.objects.get(user=request.user)
            return render(request, self.template_name, context={'profile_data': profile_data})
        except ObjectDoesNotExist:
            messages.error(request, 'No personal data!')
            return render(request, self.template_name, {'messages': messages})


class GetCVDAta(View):
    template_name = 'mainapp/cv_data.html'

    def get(self, request):
        try:
            search_query = request.GET.get('search', '')
            if search_query:
                post_object = models.CV.objects.filter(Q(subject__icontains=search_query) |
                                                       Q(extra_info__icontains=search_query))
            else:
                post_object = models.CV.objects.all()

            paginator = Paginator(post_object, 1)
            page_number = request.GET.get('page', default=1)
            page = paginator.get_page(page_number)

            is_paginated = page.has_other_pages()

            if page.has_previous():
                prev_url = '?page={}'.format(page.previous_page_number())
            else:
                prev_url = ''

            if page.has_next():
                next_url = '?page={}'.format(page.next_page_number())
            else:
                next_url = ''

            context = {
                'post_object': page,
                'is_paginated': is_paginated,
                'prev_url': prev_url,
                'next_url': next_url,
            }

            return render(request, self.template_name, context=context)
        except ObjectDoesNotExist:
            messages.error(request, 'No CV!')
            return render(request, self.template_name, {'messages': messages})


@method_decorator(login_required, name='dispatch')
class FillProfileData(View):
    template_name = 'mainapp/profile_registr.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and not models.Profile.objects.filter(user=request.user):
            prof = form.save()
            prof.user = request.user
            prof.save()
            messages.success(request, 'Data was aded!')

            from_email = settings.EMAIL_HOST_USER
            to_email = prof.email
            message = 'Welcome, {} thanks for registration!'.format(prof.name)
            send_mail('', message=message, from_email=from_email, recipient_list=[to_email])

            return redirect('/')
        else:
            messages.error(request, 'User is already exists!')
            return redirect('/', {'messages': messages})


@method_decorator(login_required, name='dispatch')
class AddCV(View):
    template_name = 'mainapp/cv_registr.html'
    class_form = CVForm

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)

        if form.is_valid() and not models.CV.objects.filter(cv__user=request.user):
            form_cv = form.save()
            form_cv.cv = models.Profile.objects.get(user=request.user)
            form_cv.save()
            messages.success(request, 'CV added to your profile!')
            return redirect('/', {'messages': messages})

        else:
            models.CV.objects.get(cv__user=request.user)
            messages.error(request, 'CV for this user already exist')
            return redirect('/', context={'messages': messages})


def get_posts_by_category(request, category_name=None):
    nodes = models.Category.objects.all()
    if category_name == None:
        posts = models.Post.objects.filter(category=nodes.first())
    else:
        posts = models.Post.objects.filter(category__name=category_name)
    return render(request, 'mainapp/post_category.html', {'nodes': nodes,
                                                          'posts': posts})


@login_required
def get_one_post(request, post_id=None):
    form = CommentForm(request.POST or None)
    if post_id is not None:
        posts = models.Post.objects.filter(id=post_id)
        comments = models.Comment.objects.filter(post__id=post_id)
        if request.POST and form.is_valid():
            comment = form.save()
            comment.post = models.Post.objects.get(id=post_id)
            comment.author = models.Profile.objects.get(user=request.user)
            comment.save()

        return render(request, 'mainapp/one-post.html', {'posts': posts,
                                                         'nodes': comments,
                                                         'form': form})
    else:
        redirect('mainapp/post_category.html')

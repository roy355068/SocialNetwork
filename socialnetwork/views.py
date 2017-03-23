from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core import serializers
from django.db import transaction
from socialnetwork.models import *
from django.http import Http404
from socialnetwork.forms import RegistrationForm, PostForm, EditForm, NameForm
from django.core.urlresolvers import reverse
import datetime
from django.http import HttpResponse
from django.contrib import messages
import json
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
@ensure_csrf_cookie
@login_required
def home(request):
    all_posts = Post.objects.all().order_by('-created_at')
    profiles = Profile.objects.exclude(picture__isnull = True).exclude(picture__exact = "")
    comments = Comment.objects.all()

    stream_stat = "Global Stream"
    if request.method == "POST":
        follow_list = []
        if 'stream' in request.POST:
            if request.POST['stream'] == "global":
                stream_stat = "Global Stream"
            elif request.POST['stream'] == "follow":
                stream_stat = "Follow Stream"
                follow_temp = Follow.objects.filter(following__username=request.user.username)
                for fol in follow_temp:
                    follow_list.append(fol.follower.username)                
                all_posts = Post.objects.filter(user__username__in=follow_list).order_by('-created_at')
                
    temp_pro = []
    for pro in profiles:
        temp_pro.append(pro.user)
    return render(request, 'socialnetwork/index.html', {'comments' : comments,'posts': all_posts, 'stream_stat': stream_stat, 'profiles': temp_pro})

@login_required
def add_comment(request, post_id):
    commented = Post.objects.get(id = post_id)
    if request.method != "POST":
        messages.error(request, 'Deletions must be done using the POST method')
    else:
        if 'content' not in request.POST or not request.POST['content']:
            pass
        #     messages.error(request, "You must eneter at least one character to post a comment")
        elif len(request.POST['content']) > 160:
            messages.error(request, "The length of comment couldn't exceed 160 characters ")
        else:
            new_comment = Comment(content = request.POST['content'], 
                                  user = request.user,
                                  commented_on = commented)
            print(new_comment.content)
            new_comment.save()

    return redirect(reverse('home'))

@login_required
def add_comment_json(request, post_id):
    commented = Post.objects.get(id = post_id)
    if request.method != "POST":
        messages.error(request, 'Comment must be done using the POST method')
    else:
        if 'content' not in request.POST or not request.POST['content']:
            pass
        #     messages.error(request, "You must eneter at least one character to post a comment")
        elif len(request.POST['content']) > 160:
            messages.error(request, "The length of comment couldn't exceed 160 characters ")
        else:
            new_comment = Comment(content = request.POST['content'], 
                                  user = request.user,
                                  commented_on = commented)
            print(new_comment.content)
            new_comment.save()
    response_text = serializers.serialize('json', Post.objects.all())
    response_text2 = serializers.serialize('json', Profile.objects.all())
    r_text3 = serializers.serialize('json', User.objects.all())
    curr_user = serializers.serialize('json', User.objects.filter(username__exact = request.user.username))
    comments = serializers.serialize('json', Comment.objects.all())
    final_data = {'comments': comments,'posts': response_text, 'profiles': response_text2, 'users': r_text3, 'curr_user':curr_user}
    final_data = json.dumps(final_data, indent = 4)
    return HttpResponse(final_data, content_type='application/json')

@login_required
def add_post(request):
    error = []
    if 'content' not in request.POST or not request.POST['content']:
        messages.error(request, "You must eneter at least one character to post a post")
    elif len(request.POST['content']) > 160:
        messages.error(request, "The length of post couldn't exceed 160 characters ")
    else:
        new_post = Post(content = request.POST['content'], 
						user = request.user)
        new_post.save()
    posts = Post.objects.all().order_by('-created_at')
    return redirect(reverse('home'))

@login_required
def add_post_json(request):
    error = ""
    if 'content' not in request.POST or not request.POST['content']:
        error =  "You must eneter at least one character to post a post"
    elif len(request.POST['content']) > 160:
        error = "The length of post couldn't exceed 160 characters "
    else:
        new_post = Post(content = request.POST['content'], 
                        user = request.user)
        new_post.save()
    response_text = serializers.serialize('json', Post.objects.all())
    response_text2 = serializers.serialize('json', Profile.objects.all())
    r_text3 = serializers.serialize('json', User.objects.all())
    curr_user = serializers.serialize('json', User.objects.filter(username__exact = request.user.username))
    comments = serializers.serialize('json', Comment.objects.all())
    final_data = {'error': error, 'comments': comments,'posts': response_text, 'profiles': response_text2, 'users': r_text3, 'curr_user':curr_user}
    final_data = json.dumps(final_data, indent = 4)
    return HttpResponse(final_data, content_type='application/json')

@login_required
def del_post(request, post_id):
    # errors = []
    if request.method != 'POST':
        messages.error(request, 'Deletions must be done using the POST method')
    else:
        try:
            post_to_delete = Post.objects.get(id = post_id, user = request.user)
            post_to_delete.delete()
        except:
            messages.error(request, "The post doesn't exist in the Post forum or user name/id mismatch with the post")
    return redirect(reverse('home'))

@login_required
def del_post_json(request, post_id):
    # errors = []
    if request.method != 'POST':
        messages.error(request, 'Deletions must be done using the POST method')
    else:
        try:
            post_to_delete = Post.objects.get(id = post_id, user = request.user)
            post_to_delete.delete()
        except:
            messages.error(request, "The post doesn't exist in the Post forum or user name/id mismatch with the post")
    response_text = serializers.serialize('json', Post.objects.all())
    response_text2 = serializers.serialize('json', Profile.objects.all())
    r_text3 = serializers.serialize('json', User.objects.all())
    curr_user = serializers.serialize('json', User.objects.filter(username__exact = request.user.username))
    comments = serializers.serialize('json', Comment.objects.all())
    final_data = {'comments': comments,'posts': response_text, 'profiles': response_text2, 'users': r_text3, 'curr_user':curr_user}
    final_data = json.dumps(final_data, indent = 4)
    return HttpResponse(final_data, content_type='application/json')

@login_required
def show_profile(request, post_user):
    context = {}
    comments = Comment.objects.all()
    profiles = Profile.objects.exclude(picture__isnull = True).exclude(picture__exact = "")
    temp_pro = []
    for pro in profiles:
        temp_pro.append(pro.user)
    try:
        # user_profile = Profile.objects.filter(user__username = post_user)
        user_profile = Profile.objects.get(user__username = post_user)
        posts = Post.objects.filter(user__username = post_user).order_by('-created_at')
        # curr_user = User.objects.filter(username = post_user)[0]
        curr_user = User.objects.get(username = post_user)

        followed = Follow.objects.filter(follower__username = post_user).filter(following__username= request.user.username)

        # one should follow/unfollow "another user"
        # so we have to exclude the following function
        # to prevent he/she to follow himself/herself
        if request.user.username == post_user:
            follow_stat = None
        # if not followed this user, display the "Follow" button
        # else if the user had been followed by current user, display the "Unfollow" button
        elif not followed.exists():
            follow_stat = True
        else:
            follow_stat = False
        context['follow_stat'] = follow_stat

        # debug prints
        # print()
        # print(str(follow_stat) + "!!!")
        # print()

        if request.method == "POST" and 'follow' in request.POST:
            if request.POST['follow'] == 'follow':
                if not followed.exists():
                    follow_temp = Follow(follower = curr_user, following = request.user)
                    follow_temp.save()
            elif request.POST['follow'] == 'unfollow' and followed.exists():
                    followed.delete()
            return redirect(reverse('show-profile', args=(post_user, )))

    # if the show-profile url contains invalid username
    # redirect to the 404 error Page. 
    except:
        raise Http404
    context['user']= post_user
    context['posts']= posts
    context['curr_user']= curr_user
    context['user_profile']= user_profile
    context['comments'] = comments
    context['pictures'] = temp_pro
    return render(request, 'socialnetwork/profile.html', context)


@login_required
# get_picture function is copied from the get_photo function in image sample code
def get_picture(request, curr_user):
    profile = get_object_or_404(Profile, user__username = curr_user)

    if not profile.picture:
        raise Http404

    return HttpResponse(profile.picture, content_type=profile.content_type)


@login_required
@transaction.atomic
def edit_profile(request):
    user = request.user
    user_profile = Profile.objects.get(user__username = user.username)
    name_form = NameForm(instance = user)
    profile_form = EditForm(instance=user_profile)
    context = {}

    # if method is GET, show the default profile editing page to user
    if request.method == "GET":
        context['name_form'] = name_form
        context['form'] = profile_form
        context['user'] = user.username
        return render(request, "socialnetwork/edit.html", context)

    elif request.method == "POST":
        name_form = NameForm(request.POST, instance = user)
        profile_form = EditForm(request.POST, request.FILES, instance = user_profile)

        if profile_form.is_valid() and name_form.is_valid():

            # if no file uploaded, save the forms and redirect the page to homepage
            if not request.FILES:
                name_form.save()
                profile_form.save()

            if profile_form.cleaned_data['picture'] and request.FILES:
                user_profile.content_type = profile_form.cleaned_data['picture'].content_type
                user_profile.save()
                name_form.save()
                profile_form.save()
        else:
            name_form.save()
            Profile.objects.filter(user__username = user.username).update(bio=request.POST['bio'], age=request.POST['age'])
            
    context['name_form'] = name_form
    context['form'] = profile_form
    context['username'] = user.username
    return redirect(reverse('home'))

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if it is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    
    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                        password = form.cleaned_data['password1'],
                                        first_name = form.cleaned_data['first_name'],
                                        last_name = form.cleaned_data['last_name'],
                                        email = form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
        Welcome to the WebApp Class Address Book.  Please click the link below to
        verify your email address and complete the registration of your account:
        http://%s%s
    """ % (request.get_host(),
            reverse('confirm', args = (new_user.username, token)))

    send_mail(subject = "Verify your email address",
              message = email_body, 
              from_email = "bochengl@andrew.cmu.edu",
              recipient_list = [new_user.email])



    new_user_profile = Profile(user = new_user,
                               age = form.cleaned_data['age'],
                               bio = form.cleaned_data['bio'])
    new_user_profile.save()

    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/need-confirmation.html', context)
    # Logs in the new user and redirects to his/her todo list
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'],)
    
    # login(request, new_user)
    # return redirect(reverse('home'))
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username = username)

    if not default_token_generator.check_token(user, token):
        raise Http404
    user.is_active = True
    user.save()
    return render(request, 'socialnetwork/confirmed.html', {})


def get_list_json(request):
    response_text = serializers.serialize('json', Post.objects.all())
    response_text2 = serializers.serialize('json', Profile.objects.all())
    r_text3 = serializers.serialize('json', User.objects.all())
    curr_user = serializers.serialize('json', User.objects.filter(username__exact = request.user.username))
    comments = serializers.serialize('json', Comment.objects.all())
    final_data = {'comments': comments,'posts': response_text, 'profiles': response_text2, 'users': r_text3, 'curr_user':curr_user}
    final_data = json.dumps(final_data, indent = 4)
    return HttpResponse(final_data, content_type='application/json')

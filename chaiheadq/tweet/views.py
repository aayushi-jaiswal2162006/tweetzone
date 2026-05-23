from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Comment, Follow, Profile
from .forms import TweetForm, CommentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from .twitter_client import post_tweet  # ✅ CORRECT IMPORT


def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet/tweet_list.html', {'tweets': tweets, 'user': request.user})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()

            # Send tweet to Twitter
            tweet_id = post_tweet(tweet.content)
            print(f"📤 Sent to Twitter with ID: {tweet_id}")

            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet/tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet/tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet/tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('tweet_list')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    comments = tweet.comments.all().order_by('-created_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=tweet.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_detail', tweet_id=tweet_id)
    else:
        form = CommentForm()

    return render(request, 'tweet/tweet_detail.html', {
        'tweet': tweet,
        'comments': comments,
        'form': form,
        'is_following': is_following,
    })


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=profile_user)
    following = Follow.objects.filter(follower=profile_user)
    tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = followers.filter(follower=request.user).exists()

    context = {
        'profile_user': profile_user,
        'tweets': tweets,
        'followers': followers,
        'following': following,
        'followers_count': followers.count(),
        'following_count': following.count(),
        'is_following': is_following,
    }
    return render(request, 'tweet/profile.html', context)


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('profile_view', username=username)

    follow_obj = Follow.objects.filter(follower=request.user, following=target_user).first()
    if follow_obj:
        follow_obj.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect('profile_view', username=username)


@login_required
def tweet_like_toggle(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user
    if user in tweet.likes.all():
        tweet.likes.remove(user)
    else:
        tweet.likes.add(user)
    return redirect(request.META.get('HTTP_REFERER', 'tweet_list'))

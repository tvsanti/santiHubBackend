from django.http import JsonResponse
from django.shortcuts import render

from .models import Post
from account.models import User

from .serializers import PostSerializer
from account.serializers import UserSerializer

from rest_framework.decorators import api_view
from .forms import PostForms


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForms(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({
        'error': 'something went wrong'
    })

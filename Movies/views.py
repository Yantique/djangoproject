from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.http import HttpResponse
from djangoProject import settings
from .models import *


def get_video(request, file_name):
    file_root = settings.MEDIA_ROOT + file_name
    with open(file_root, 'rb') as video_file:
        response = HttpResponse(video_file.read())
        response['Content_Type'] = 'video/mp4'
    return response


class MainView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        tag = request.GET.get('tag')
        videos = None
        if q:
            videos = Video.objects.filter(title__contains=q)
        elif tag:
            video_tags = VideoTag.objects.filter(tag__name__iexact=tag)
            videos = set([tag.video for tag in video_tags])
        else:
            videos = Video.objects.all()
        return render(request, 'movies/index.html', context={'videos': videos})


class UploadView(View):
    message = "None of the fields can be empty! Try again."

    def get(self, request, *args, **kwargs):
        return render(request, "movies/upload.html")

    def post(self, request, *args, **kwargs):
        tags = request.POST.get("tags")
        title = request.POST.get("title")
        if tags and request.FILES and title:
            new_tag = Tag.objects.create(name=tags)
            new_video = Video.objects.create(title=title, file=request.FILES['video'])
            new_video_tag = VideoTag.objects.create(video=new_video, tag=new_tag)
            new_video_tag.save()
            return redirect("/tube/")
        else:
            context = {"user": request.user, "message": self.message}
            return render(request, "movies/upload.html", context=context)


class WatchView(View):
    def get(self, request, video_id, *args, **kwargs):
        video = Video.objects.get(id=video_id)
        video_tags = VideoTag.objects.filter(video__title__iexact=video.title)
        tags = set([vid.tag for vid in video_tags])
        context = {'video': video, 'tags': tags}
        return render(request, "movies/watch.html", context=context)


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'movies/signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'movies/login.html'

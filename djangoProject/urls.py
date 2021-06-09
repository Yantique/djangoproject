from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.urls import path
from Movies.views import *


urlpatterns = [
    path('', RedirectView.as_view(url='/tube/')),
    path('tube/', MainView.as_view()),
    path('tube/upload/', UploadView.as_view()),
    path('tube/watch/<int:video_id>/', WatchView.as_view()),
    path('tube/<str:file_name>', get_video),
    path('admin/', admin.site.urls),
    path('login/', MyLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', MySignupView.as_view()),
]

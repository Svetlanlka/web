"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static
from django.conf import settings


from app import views
urlpatterns = [
    path('', views.index, name='main'),
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name = 'ask'),
    path('hot_questions/', views.hot_questions, name='hot_questions'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('new_questions/', views.new_questions, name='new_questions'),
    path('questions/<int:id>/', include([
        path('', views.one_question, name='one_question'),
        path('vote/', views.question_vote, name='question_vote'),
    ])),
    path('register/', views.register, name = 'register'),
    path('search_tag/<slug:tag_name>/', views.search_tag, name='search_tag'),
    path('settings/', views.settings, name = 'settings'),
    path('answer_vote/', views.answer_vote, name='answer_vote'),
    path('change_correct/', views.change_correct, name='change_correct'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
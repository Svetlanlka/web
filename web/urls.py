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

from django.conf.urls.static import static
from django.conf import settings


from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name = 'ask'),
    path('hot/', views.hot_questions, name='hot'),
    path('login/', views.login, name = 'login'),
    path('new/', views.new_questions, name='new'),
    path('questions/<int:id>/', views.one_question, name='one_question'),
    path('register/', views.register, name = 'register'),
    path('search_tag/<slug:tag_name>/', views.search_tag, name='search_tag'),
    path('settings/', views.settings, name = 'settings'),
    path('', views.index),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
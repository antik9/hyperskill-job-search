"""jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path

from web.views import (
    ResumeView, VacancyView, LoginView, SignupView,
    do_logout, get_index, ProfileView, ResumeDetailView,
    VacancyDetailView,
)


urlpatterns = [
    re_path('apply_resume/(?P<pk>[0-9]+)/?', ResumeDetailView.as_view(), name='apply_resume'),
    re_path('apply_vacancy/(?P<pk>[0-9]+)/?', VacancyDetailView.as_view(), name='apply_vacancy'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', do_logout, name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('resumes', ResumeView.as_view(), name='resume_list'),
    path('signup', SignupView.as_view(), name='signup'),
    path('vacancies', VacancyView.as_view(), name='vacancy_list'),
    path('', get_index, name='main'),
]

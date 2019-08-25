from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http.response import Http404
from django.shortcuts import redirect, render_to_response, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import (
    Application, Resume, Vacancy, User,
)

AuthenticationForm.next = reverse_lazy('resumes')


def do_logout(request, *args, **kwargs):
    logout(request)
    return redirect(reverse('main'), context={'request': request})


def get_index(request, *args, **kwargs):
    return render_to_response('index.html', context={'request': request})


class ProfileView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'web/profile.html')
        else:
            raise Http404


class ResumeView(ListView):
    model = Resume
    paginate_by = 100

    def post(self, request, *args, **kwargs):
        self.model.objects.create(
            text=request.POST.get('text'), author=request.user
        )
        return redirect(reverse('profile'))


class ResumeDetailView(DetailView):
    model = Resume

    def post(self, request, pk, *args, **kwargs):
        try:
            resume = Resume.objects.get(pk=pk)
            vacancy_id = request.POST.get('vacancy_id')
            application = Application.objects.filter(
                resume=resume, vacancy_id=vacancy_id
            ).first()
            if application:
                application.confirmed_by_employer = True
                application.save()
            else:
                Application.objects.create(
                    resume=resume, vacancy_id=vacancy_id, confirmed_by_employer=True
                )
            return redirect(request.POST.get('next', reverse('resume_list')))
        except Resume.DoesNotExist:
            raise Http404


class VacancyView(ListView):
    model = Vacancy
    paginate_by = 100

    def post(self, request, *args, **kwargs):
        self.model.objects.create(
            text=request.POST.get('text'), author=request.user
        )
        return redirect(reverse('profile'))


class VacancyDetailView(DetailView):
    model = Vacancy

    def post(self, request, pk, *args, **kwargs):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            resume_id = request.POST.get('resume_id')
            application = Application.objects.filter(
                resume_id=resume_id, vacancy=vacancy
            ).first()
            if application:
                application.confirmed_by_candidate = True
                application.save()
            else:
                Application.objects.create(
                    resume_id=resume_id, vacancy=vacancy, confirmed_by_candidate=True
                )
            return redirect(request.POST.get('next', reverse('vacancy_list')))
        except Resume.DoesNotExist:
            raise Http404


class LoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'login.html'


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

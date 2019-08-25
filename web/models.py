from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Resume(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Candidate')
    text = models.TextField(verbose_name='resume text')


class Vacancy(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Employer')
    text = models.TextField(verbose_name='vacancy text')


class Application(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Application')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name='Vacancy')
    confirmed_by_candidate = models.BooleanField(default=False)
    confirmed_by_employer = models.BooleanField(default=False)

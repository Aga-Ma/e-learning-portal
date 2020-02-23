from django.urls import reverse
from django.conf import settings
from django.db import models

from students.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse('course_detail', args=(self.id,))

    def __str__(self):
        return self.name


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    number = models.IntegerField()
    test = models.TextField()

    class Meta:
        unique_together = ('course', 'number', )

    def __str__(self):
        return self.title

    def get_test_url(self):
        return reverse('do_test', args=(self.id,))

    def get_absolute_url(self):
        return reverse('do_test', args=(self.id,))

    def get_next_section_url(self):
        next_section = Section.objects.get(number=self.number+1)
        return reverse('do_section', args=(next_section.id,))


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    correct = models.BooleanField()

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'user', )

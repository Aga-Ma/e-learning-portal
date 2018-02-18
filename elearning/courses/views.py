from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, ListView
from django.shortcuts import render, redirect

from courses.models import Course, UserAnswer, Section, Question
from courses.forms import CourseForm


class CourseDetailView(DetailView):
    model = Course


course_detail = CourseDetailView.as_view()


class CourseListView(ListView):
    model = Course
    queryset = Course.objects.prefetch_related('students')


course_list = CourseListView.as_view()


class CourseAddView(CreateView):
    model = Course
    fields = '__all__'


course_add = CourseAddView.as_view()


def do_section(request, section_id):
    section = Section.objects.get(id=section_id)
    return render(request, 'courses/do_section.html', {
        'section': section,
    })


def do_test(request, section_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue
            # {'question-1': '2'}
            question_id = key.split('-')[1]
            answer_id = request.POST.get(key)
            data[question_id] = answer_id
        perform_test(request.user, data, section)
        return redirect(reverse('show_results', args=(section.id,)))
    return render(request, 'courses/do_test.html', {
        'section': section,
    })


def perform_test(user, data, section):
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,
                                  question__section=section).delete()
        for question_id, answer_id in data.items():
            question = Question.objects.get(id=question_id)
            answer_id = int(answer_id)
            if answer_id not in question.answer_set.values_list('id', flat=True):
                raise SuspiciousOperation('Answer is not valid for this question')
            UserAnswer.objects.create(user=user,
                                      question=question,
                                      answer_id=answer_id,
            )


def calculate_score(user, section):
    questions = Question.objects.filter(section=section)
    correct_answers = UserAnswer.objects.filter(
        user=user,
        question__section=section,
        answer__correct=True
    )
    return (correct_answers.count() / questions.count()) * 100


def show_results(request, section_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    return render(request, 'courses/show_results.html', {
        'section': section,
        'score': calculate_score(request.user, section)
    })

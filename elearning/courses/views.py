from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


from courses.models import Course, UserAnswer, Section, Question
from courses.forms import CourseForm


def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course_detail.html', {
            'course': course,
        })


def course_list(request):
    courses = Course.objects.prefetch_related('students')
    return render(request, 'course_list.html', {
        'courses': courses,
    })


def course_add(request):
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
            return HttpResponseRedirect(new_course.get_absolute_url())
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {
        'form': form,
    })


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
        with transaction.atomic():
            UserAnswer.objects.filter(user=request.user,
                                      question__section=section).delete()
            for key, value in request.POST.items():
                if key == 'csrfmiddlewaretoken':
                    continue
                # {'question-1': '2'}
                question_id = key.split('-')[1]
                question = Question.objects.get(id=question_id)
                answer_id = int(request.POST.get(key))
                if answer_id not in question.answer_set.values_list('id', flat=True):
                    raise SuspiciousOperation('Answer is not valid for this question')
                UserAnswer.objects.create(user=request.user,
                                          question=question,
                                          answer_id=answer_id,)
        return redirect(reverse('show_results', args=(section.id,)))
    return render(request, 'courses/do_test.html', {
        'section': section,
    })
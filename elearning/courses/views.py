from django.shortcuts import render
from django.http import HttpResponseRedirect


from courses.models import Course
from courses.forms import CourseForm


def course_detail(request, course_id):
    print(Course.objects.all())
    course = Course.objects.get(id=course_id)
    return render(request, 'course_detail.html', {
            'course': course,
        })


def course_list(request):
    courses = Course.objects.all()
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

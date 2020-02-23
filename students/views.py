from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from courses.models import Course
from courses.views import calculate_score

from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'students/signup.html', {'form': form})


def get_all_scores_for_user(user):
    scores = []
    for course in Course.objects.all():
        course_scores = []
        for section in course.section_set.order_by('number'):
            course_scores.append((section, calculate_score(user, section),))
        scores.append((course, course_scores),)
    return scores


def student_detail(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    student = request.user
    return render(request, 'students/student_detail.html', {
        'student': student,
        'scores': get_all_scores_for_user(student),
    })

from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def student_detail(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    student = request.user
    return render(request, 'students/student_detail.html', {
        'student': student,
    })

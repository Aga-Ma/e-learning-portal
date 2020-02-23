from django import forms

from courses.models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', ]
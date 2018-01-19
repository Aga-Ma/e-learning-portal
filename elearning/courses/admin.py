from django.contrib import admin

from courses.models import Course


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)

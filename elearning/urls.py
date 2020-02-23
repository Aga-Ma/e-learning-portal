"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.contrib import admin

from rest_framework import routers

from students.views import signup, student_detail
from courses.views import course_detail, course_list, course_add, do_section, do_test, show_results, SectionViewSet
from api.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sections', SectionViewSet)


urlpatterns = [
    re_path(r'^$', course_list, name='home'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^signup/$', signup, name='signup'),
    re_path('^', include(('django.contrib.auth.urls', 'user'), namespace='auth')),
    re_path(r'^course_detail/(?P<pk>\d+)/$', course_detail, name='course_detail'),
    re_path(r'^course_add/$', course_add, name='course_add'),
    re_path(r'^section/(?P<section_id>\d+)/$', do_section, name='do_section'),
    re_path(r'^section/(?P<section_id>\d+)/test/$', do_test, name='do_test'),
    re_path(r'^section/(?P<section_id>\d+)/results/$', show_results, name='show_results'),
    re_path(r'^student_detail/$', student_detail, name='student_detail'),
    re_path(r'^api/', include(router.urls)),
]

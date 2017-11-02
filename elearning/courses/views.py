from django.http import HttpResponse


def my_first_view(request, who):
    return HttpResponse("Hello %s!" % who)

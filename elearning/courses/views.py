from django.shortcuts import render

def my_first_view(request, who):
    return render(request, 'hello.html', {
            'who': who,
        })

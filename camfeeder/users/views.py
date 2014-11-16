from django.shortcuts import render

from .models import User

def list_(request):
    users = User.objects.all()

    return render( 'users/list.html', {
        'users' : users,
    })


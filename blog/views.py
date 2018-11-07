from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def kod(request):
    if request.GET.get('btn'):
        profil = get_object_or_404(Profile, user=request.user)
        xd = request.GET.get('inputed_code')
        if xd == 'polska' or 'usa' or 'germany':
            messages.success(request, f'Prawidlowy kod!!')
            profil.points += 100
            profil.usedpoints += " , " + xd
        else:
            messages.warning(request, f'Zly kod!!')

        profil.save(update_fields=["points", "usedpoints"])
        return render(request, 'users/profile.html')

    else:
        return render(request, 'blog/kod.html')


def home(request):
    admin = get_object_or_404(Profile, usedpoints="dumbldore")
    if request.GET.get('dworcowa3'):
        if admin.dworcowa3 == 1:
            messages.warning(request, f'Budynek juz kupiony')
            return render(request, 'blog/home.html')
        profil = get_object_or_404(Profile, user=request.user)
        messages.success(request, f'Kupiles budynek')
        admin.dworcowa3 = 1
        profil.dworcowa3 = 1
        profil.save()
        admin.save()
        return render(request, 'blog/home.html')

    if request.GET.get('dworcowa10'):
        if admin.dworcowa10 == 1:
            messages.warning(request, f'Budynek juz kupiony')
            return render(request, 'blog/home.html')
        profil = get_object_or_404(Profile, user=request.user)
        messages.success(request, f'Kupiles budynek')
        admin.dworcowa10 = 1
        profil.dworcowa10 = 1
        profil.save()
        admin.save()
        return render(request, 'blog/home.html')

    if request.GET.get('dworcowa13'):
        if admin.dworcowa13 == 1:
            messages.warning(request, f'Budynek juz kupiony')
            return render(request, 'blog/home.html')
        profil = get_object_or_404(Profile, user=request.user)
        messages.success(request, f'Kupiles budynek')
        admin.dworcowa13 = 1
        profil.dworcowa13 = 1
        profil.save()
        admin.save()
        return render(request, 'blog/home.html')

    else:
        return render(request, 'blog/home.html', {'admin': admin})
# Create your views here.

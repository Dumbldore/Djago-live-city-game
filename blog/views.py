from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from users.models import Patrol
from users.models import Building
from users.models import Big_Building
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from background_task import background
from django.utils import timezone


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@background(schedule=1)
def hello(user_id, generated_people, generated_points):
    patrol = get_object_or_404(Patrol, id=user_id)
    patrol.people += generated_people
    patrol.points += generated_points
    patrol.save()


@background(schedule=1)
def background_addpoints(xd):
    patrol1 = get_object_or_404(Patrol, id=int(xd[1]))
    patrol1.people += 50
    patrol1.save()
    patrol2 = get_object_or_404(Patrol, id=int(xd[2]))
    patrol2.people += 50
    patrol2.save()
    patrol3 = get_object_or_404(Patrol, id=int(xd[3]))
    patrol3.people += 50
    patrol3.save()
    patrol4 = get_object_or_404(Patrol, id=int(xd[4]))
    patrol4.people += 50
    patrol4.save()


def kod(request):
    if request.GET.get('btn'):
        profil = get_object_or_404(Patrol, user=request.user)
        xd = request.GET.get('inputed_code')
        if xd == 'polska' or xd == 'usa':
            messages.success(request, f'Prawidlowy kod!!')
            profil.points += 100
            profil.usedcodes += " , " + xd
        else:
            messages.warning(request, f'Zly kod!!')

        profil.save(update_fields=["points", "usedcodes"])
        return render(request, 'blog/kod.html')

    else:
        return render(request, 'blog/kod.html')


def home(request):
    context = {
        'buildings': Building.objects.all(),
        'bigbuildings': Big_Building.objects.all(),
        'posts': Post.objects.all(),
        'patrol': get_object_or_404(Patrol, user=request.user)
    }
    profil = get_object_or_404(Patrol, user=request.user)
    for each in Building.objects.all():
        building = each
        if request.GET.get(building.name):
            if building.built == 1:
                messages.warning(request, f'Budynek juz zbudowany')
                return render(request, 'blog/home.html')
            else:
                if profil.points >= building.cost:
                    messages.success(request, f'Brawo!, zbudowales budynek')
                    building.built = 1
                    building.patrol = profil
                    profil.built_buildings += building.name
                    profil.number_of_built_buildings += 1
                    building.date=timezone.now()
                    profil.points -= building.cost
                    profil.save()
                    building.save()
                    hello(profil.id,building.generate_people, building.generate_points, repeat=60)
                    return render(request, 'blog/home.html', context)
                else:
                    messages.warning(request, f'Masz za malo pieniedzy!')
                    return render(request, 'blog/home.html')

    for each in Big_Building.objects.all():
        bigbuilding = each
        if request.GET.get(bigbuilding.name):
            if bigbuilding.how_much_built == bigbuilding.size:
                messages.warning(request, f'Budynek juz zbudowany')
                return render(request, 'blog/home.html')
            else:
                if profil.points >= 500:
                    messages.success(request, f'Brawo!, Dzieki Tobie odbudujemy Gdansk!')
                    bigbuilding.how_much_built += 1
                    bigbuilding.patrol += str(profil.user.id)
                    profil.built_buildings += bigbuilding.name
                    profil.number_of_built_buildings += 1
                    profil.points -= 500
                    if bigbuilding.how_much_built == bigbuilding.size:
                        background_addpoints(bigbuilding.patrol, repeat=60*10)
                    profil.save()
                    bigbuilding.save()
                    return render(request, 'blog/home.html', context)
                else:
                    messages.warning(request, f'Masz za malo pieniedzy!')
                    return render(request, 'blog/home.html')


        else:
            return render(request, 'blog/home.html', context)
# Create your views here.

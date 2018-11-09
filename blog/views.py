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
    return render(request, "blog/about.html", {"title": "About"})


SMALL_BUILDING_BUILD_TIME = 60 * 10  # sec
BIG_BUILDING_BUILD_TIME = 60 * 30  # sec

SMALL_BUILDING_GEN_INTERVAL = 60
BIG_BUILDING_GEN_INTERVAL = 60 * 10


@background(schedule=SMALL_BUILDING_BUILD_TIME)
def background_gen_small_points(
    building_id, user_id, generated_people, generated_points
):
    patrol = get_object_or_404(Patrol, id=user_id)
    patrol.people += generated_people
    patrol.points += generated_points
    patrol.save()
    print(
        building_id,
        "generated (pts, ppl)",
        generated_people,
        generated_points,
        patrol.user.username,
    )


@background(schedule=BIG_BUILDING_BUILD_TIME)
def background_gen_big_points(
    building_id, patrol_ids, generated_people, generated_points
):
    """Dodaje punkty wszyskim budowniczym"""
    patrol_ids = list(map(lambda s: s.strip(), str(patrol_ids).split(",")))

    if len(patrol_ids) == 4:
        for patrol_id in patrol_ids:
            patrol = get_object_or_404(Patrol, id=int(patrol_id))
            patrol.people += generated_people
            patrol.points += generated_points
            patrol.save()
            print(
                building_id,
                "(big) generated (pts, ppl)",
                generated_people,
                generated_points,
                patrol.user.username,
            )
    else:
        print("Not built")


def kod(request):
    """
    Pozwala użytwkownikowi wpisać, który daje mu jakiś benefit
    """
    codes = {"polska": 200, "usa": 100}

    if request.GET.get("btn"):
        profil = get_object_or_404(Patrol, user=request.user)
        requested_code = request.GET.get("inputed_code")

        used_codes = list(map(lambda s: s.strip(), str(profil.usedcodes).split(",")))

        if requested_code in codes and requested_code not in used_codes:
            messages.success(request, f"Prawidlowy kod!!")
            profil.points += codes[requested_code]
            profil.usedcodes += "," + requested_code
        else:
            messages.warning(request, f"Zly kod!!")

        profil.save(update_fields=["points", "usedcodes"])
        return render(request, "blog/kod.html")

    else:
        return render(request, "blog/kod.html")


def home(request):
    context = {
        "buildings": Building.objects.all(),
        "bigbuildings": Big_Building.objects.all(),
        "posts": Post.objects.all(),
        "patrol": get_object_or_404(Patrol, user=request.user),
    }
    profil = get_object_or_404(Patrol, user=request.user)
    for each in Building.objects.all():
        building = each
        if request.GET.get(building.name):
            if building.built == 1:
                messages.warning(request, f"Budynek juz zbudowany")
                return render(request, "blog/home.html")
            else:
                if profil.points >= building.cost:
                    messages.success(request, f"Brawo!, zbudowales budynek")
                    building.built = 1
                    building.patrol = profil
                    profil.built_buildings += building.name
                    profil.number_of_built_buildings += 1
                    building.date = timezone.now()
                    profil.points -= building.cost
                    profil.save()
                    building.save()
                    background_gen_small_points(
                        building_id=building.id,
                        user_id=profil.id,
                        generated_people=building.generate_people,
                        generated_points=building.generate_points,
                        repeat=SMALL_BUILDING_GEN_INTERVAL,
                    )
                    return render(request, "blog/home.html", context)
                else:
                    messages.warning(request, f"Masz za malo pieniedzy!")
                    return render(request, "blog/home.html")

    for each in Big_Building.objects.all():
        bigbuilding = each
        if request.GET.get(bigbuilding.name):
            if bigbuilding.how_much_built == bigbuilding.size:
                messages.warning(request, f"Budynek juz zbudowany")
                return render(request, "blog/home.html")
            else:
                if profil.points >= bigbuilding.cost:
                    messages.success(
                        request, f"Brawo!, Dzieki Tobie odbudujemy Gdansk!"
                    )
                    bigbuilding.how_much_built += 1
                    bigbuilding.patrol += str(profil.user.id)
                    profil.built_buildings += bigbuilding.name
                    profil.number_of_built_buildings += 1
                    profil.points -= bigbuilding.cost
                    if bigbuilding.how_much_built == bigbuilding.size:
                        background_gen_big_points(
                            building_id=bigbuilding.id,
                            patrol_ids=bigbuilding.patrol,
                            generated_people=bigbuilding.generate_people,
                            generated_points=bigbuilding.generate_points,
                            repeat=BIG_BUILDING_GEN_INTERVAL,
                        )
                    profil.save()
                    bigbuilding.save()
                    return render(request, "blog/home.html", context)
                else:
                    messages.warning(request, f"Masz za malo pieniedzy!")
                    return render(request, "blog/home.html")

        else:
            return render(request, "blog/home.html", context)


# Create your views here.

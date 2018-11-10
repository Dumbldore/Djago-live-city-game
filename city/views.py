from django.shortcuts import render
from .models import Building, Patrol2 as Patrol, BonusCode, UsedBonusCode
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

def progress(b):
    s = b.shareholders.all()
    count = s.count()
    max = b.max_shares
    return {
        "done": b.is_built(),
        "can_buy": b.can_buy(),
        "shares_percent": int(count / max * 100),
        "max_shares": max,
        "shares": count,
        "shares_left": max - count,
        "shareholders": [s.name for s in s],
    }


# Create your views here.
def building_detail(request, building_id):
    try:
        b = Building.objects.get(id=building_id)
    except Building.DoesNotExist:
        raise Http404("Building does not exist")

    s = b.shareholders.all()

    progress = {
        "done": b.is_built(),
        "shares_percent": int(s.count() / b.max_shares * 100),
    }
    return render(
        request,
        "blog/building.html",
        {"building": b, "shareholders": s, "progress": progress},
    )


def building_list(request):
    buy_building_id = request.POST.get("buy_building")
    if buy_building_id:
        building = Building.objects.get(id=buy_building_id)
        patrol = get_object_or_404(Patrol, user=request.user)
        if building.can_buy() and building.share_cost < patrol.money:
            building.buy_share_for(patrol)
            messages.success(request, f"Kupiono {building.name}!")
        else:
            messages.warning(
                request, f"Nie można kupić {building.name}! Za mało pieniędzy/miejsc"
            )

    return render(
        request,
        "blog/list.html",
        {
            "buildings": [
                (b, b.shareholders.all(), progress(b)) for b in Building.objects.all()
            ]
        },
    )


@login_required
def kod(request):
    """
    Pozwala użytwkownikowi wpisać, który daje mu jakiś benefit
    """
    patrol = get_object_or_404(Patrol, user=request.user)

    if request.GET.get("btn") and request.user.is_authenticated:
        requested_code = request.GET.get("inputed_code")

        try:
            bonus_code = BonusCode.objects.get(code=requested_code)
        except BonusCode.DoesNotExist:
            messages.warning(request, f"Podano błędny kod")
        else:
            if UsedBonusCode.objects.filter(
                    patrol=patrol, bonus_code=bonus_code
            ).exists():
                messages.warning(
                    request, f"Podano kod został wykorzystany przez {patrol}"
                )
            else:
                patrol.money += bonus_code.value
                used_code = UsedBonusCode(patrol=patrol, bonus_code=bonus_code)
                patrol.save()
                used_code.save()

                messages.success(request, f"Dodano {bonus_code.value}")

    queryset = UsedBonusCode.objects.filter(patrol=patrol)
    used_codes = [c.bonus_code for c in queryset]

    return render(request, "blog/kod.html", {"used_bonus_codes": used_codes})


def stats(request):
    total = Building.objects.count()
    built = sum(1 for b in Building.objects.all() if b.is_built())

    city_built_percent = built / total * 100

    total_ppl = Patrol.objects.aggregate(total_ppl=Sum('people'))["total_ppl"]

    return render(request, "blog/stats.html", {"city_built_percent": city_built_percent, "total_ppl": int(total_ppl)})


def patrol_detail(request, patrol_id):
    patrol = Patrol.objects.get(id=patrol_id)
    buildings = set(s.building for s in patrol.share_set.all())
    shares = patrol.share_set.all()
    money_generated = 0
    people_generated = 0

    for share in shares:
        if share.building.is_built():
            # logger.info(share.building.name, share.building.generate_points)
            money_generated += (
                share.building.generate_points
            )
            people_generated += (
                share.building.generate_people
            )
    return render(request, "blog/patrol.html", {"patrol": patrol, "buildings": buildings, "money_generated" : money_generated, "people_generated" : people_generated})

from django.shortcuts import render
from .models import Building, Patrol2 as Patrol
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages


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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def profile(request):
        if request.GET.get('mybtn'):
            profil = get_object_or_404(Profile, user=request.user)
            profil.points += 10
            profil.save(update_fields=["points"])
            messages.success(request, f'Account created for!')

            return render(request, 'users/profile.html')

        else:
            return render(request, 'users/profile.html')


# Profile.objects.update(points=20)

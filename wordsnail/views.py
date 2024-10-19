from django.shortcuts import render, redirect
from django.contrib import messages

from wordsnail.models import Shop, Rating
from wordsnail.utils import register_new_user, change_skin, add_skin, getinfo, postrequest
from wordsnail.forms import RegisterUserForm
from django.contrib.auth.decorators import login_required


__all__ = (
    "home",
    "register",
    "raiting",
    "shop",
)

def home(request):
    return render(request, "wordsnail/home.html")


def register(request):
    if request.method == "POST":
        register_new_user(request)
        messages.success(request, "Registration successful.")
        redirect("index")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = RegisterUserForm()
    return render(request, "registration/register.html", {'form': form})


def raiting(request):
    all_ratings = Rating.objects.all().order_by('-rating')

    user_place = None
    current_user_rating = None

    if request.user.is_authenticated:
        for index, rating in enumerate(all_ratings):
            rating.place = index + 1
            if rating.user_id == request.user:
                user_place = index + 1
                current_user_rating = rating

    return render(request, 'wordsnail/rating.html', {
        'r': all_ratings,
        'current_user_rating': current_user_rating,
        'user_place': user_place,
    })
def shop(request):  # страница магазина
    user = request.user
    if not user.is_authenticated:
        return redirect('index')

    things_in_shop, current_user_id, id_lis, user_profile = getinfo(user)
    if request.method == 'POST':
        return postrequest(request, id_lis, current_user_id)

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": user_profile.money,
                                                   "skin": user_profile.current_skin})



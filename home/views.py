from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import LOCATION_CHOICES, Profile, COORDS
from cart.models import Order, Item

from django.contrib.auth.decorators import login_required

def index(request):
    template_data = {'title': 'Movies Store'}
    context = {'template_data': template_data}

    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            city = request.POST.get('location')
            if not profile.location_chosen and city in COORDS:
                profile.location = city
                profile.location_chosen = True
                profile.save()
            return redirect('home.index')
        context['profile'] = profile
        context['location_choices'] = LOCATION_CHOICES

    return render(request, 'home/index.html', context)

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

@login_required
def map_view(request):
    profile,thingy=Profile.objects.get_or_create(user=request.user)
    if not profile.location_chosen:
        return redirect('home.index')
    loc=profile.location
    lat, lng = COORDS[loc]
    rows = (Item.objects
            .values('order__user__profile__location', 'movie__id', 'movie__name')
            .annotate(total=Sum('quantity'))
            .order_by('order__user__profile__location', '-total', 'movie__name'))

    top = {}
    for r in rows:
        c = r['order__user__profile__location']
        if c is None or c not in COORDS:
            continue
        if c not in top:
            clat, clng = COORDS[c]
            top[c] = {'city': c, 'lat': clat, 'lng': clng,
                      'movie': r['movie__name'], 'movie_id': r['movie__id'],
                      'total': r['total'], 'you_bought': None}
    if loc in top:
        top[loc]['you_bought'] = (
            Item.objects.filter(order__user=request.user,
                                movie_id=top[loc]['movie_id'])
            .aggregate(n=Sum('quantity'))['n'] or 0)

    return render(request, 'home/map.html', {
        'lat': lat, 'lng': lng,
        'user_city': loc,
        'cities': list(top.values()),
    })
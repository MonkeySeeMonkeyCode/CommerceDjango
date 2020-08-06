from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import User, Listing, CurrentBid, Watchlist


def index(request):
    listing = Listing.objects.all().filter(active=True)
    return render(request, "auctions/index.html", {
        'listing': listing,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'init_bid', 'image', 'category']
        labels = {
            'init_bid' : _('Initial Bid')
        }

class BidForm(ModelForm):
    class Meta:
        model = CurrentBid
        fields = '__all__'

def createlisting(request):
    if request.method == "GET":
        form = ListingForm()
        return render(request, "auctions/createlisting.html", {
            "title": "Create new listing",
            "form": form,
        })
    if request.method == "POST":
        form = ListingForm(request.POST)
        listing = form.save(commit=False)
        listing.active = True
        listing.createdby = request.username
        bidform = BidForm()
        bid = bidform.save(commit=False)
        bid.amount = listing.init_bid
        bid.user = request.user
        bid.save()
        listing.currentbid = bid
        listing.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse("index"))

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        category = listing.category.all()
        watchlist = Watchlist.objects.get(user=request.user,listing=listing)
    except Listing.DoesNotExist:
        raise Http404("Listing no found.")
    except Watchlist.DoesNotExist:
        watchlist = ""
    return render(request, "auctions/listingdetail.html", {
        "listing": listing,
        "category": category,
        "watchlist": watchlist,
    })

class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = '__all__'

def watchlist(request):
    listing = Listing.objects.get(pk=request.POST['id'])
    action = request.POST['action']
    user = request.user
    if action == "add":
        watchlist = Watchlist(user=user, listing=listing)
        watchlist.save()
    if action == "remove":
        watchlist = Watchlist.objects.get(user=user.id, listing=request.POST['id'])
        watchlist.delete()
    return HttpResponseRedirect(reverse("listing", args=(request.POST['id'],)))
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import User, Listing, CurrentBid


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
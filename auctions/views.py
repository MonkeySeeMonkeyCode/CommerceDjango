from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.forms import modelformset_factory
from django import forms

from .models import User, Listing, CurrentBid, Watchlist, Comment, Category


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
        fields = ['amount','user']
        labels = {
            'amount' : _('Bid')
        }
        widgets = {'user': forms.HiddenInput()}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['description','user']
        labels = {
            'description': _(''),
            'user': _('Posted by: ')
        }

@login_required(login_url="/login")
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
        listing.createdby = request.user
        bidform = BidForm()
        bid = bidform.save(commit=False)
        bid.amount = listing.init_bid
        bid.user = request.user
        bid.initial = "True"
        bid.save()
        listing.currentbid = bid
        listing.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="/login")
def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing no found.")
    category = listing.category.all()
    try:
        bid = CurrentBid.objects.get(pk=listing.currentbid.id)
    except CurrentBid.DoesNotExist:
        raise Http404("Something wrong with the bidding system happened")
    bidform = BidForm(instance=bid)
    try:
        watchlist = Watchlist.objects.get(user=request.user,listing=listing)
    except Watchlist.DoesNotExist:
        watchlist = ""
    try:
        comment = Comment.objects.all().filter(listing=listing)
    except Comment.DoseNotExist:
        comment = ""
    return render(request, "auctions/listingdetail.html", {
        "listing": listing,
        "category": category,
        "watchlist": watchlist,
        "bid": bid,
        "bidform": bidform,
        "comments": comment,
    })

class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = '__all__'

@login_required(login_url="/login")
def watchlist(request):
    if request.method == "GET":
        watchlist = Watchlist.objects.all().filter(user=request.user)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })
    if request.method == "POST":
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

@login_required(login_url="/login")
def placebid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST['id'])
        originalBid = CurrentBid.objects.get(pk=listing.currentbid.id)
        if originalBid.initial and int(request.POST['amount']) >= listing.init_bid or int(request.POST['amount']) > int(originalBid.amount):
            bidForm = BidForm(request.POST, instance=originalBid)
            newBid = bidForm.save(commit=False)
            newBid.user = request.user
            newBid.initial = "False"
            newBid.save()
            return HttpResponseRedirect(reverse("listing", args=(request.POST['id'],)))
        else:
            try:
                listing = Listing.objects.get(id=request.POST['id'])
                category = listing.category.all()
                bid = BidForm(instance=CurrentBid.objects.get(pk=listing.currentbid.id))
                watchlist = Watchlist.objects.get(user=request.user,listing=listing)
            except Listing.DoesNotExist:
                raise Http404("Listing no found.")
            except Watchlist.DoesNotExist:
                watchlist = ""
            return render(request, "auctions/listingdetail.html", {
                "listing": listing,
                "category": category,
                "watchlist": watchlist,
                "bid": bid,
                "biderror": "Bid unsuccessful. Amount needs to be greater than current price."
            })

@login_required(login_url="/login")
def closelisting(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST['id'])
        if listing.createdby == request.user:
            form = ListingForm(instance=listing)
            item = form.save(commit=False)
            item.active = False
            item.save()
    return HttpResponseRedirect(reverse("listing", args=(request.POST['id'],)))

@login_required(login_url="/login")
def comment(request):
    if request.method == "POST":
        comment = Comment(description=request.POST['comment'], user=request.user, listing=Listing.objects.get(pk=request.POST['id']))
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=(request.POST['id'],)))

@login_required(login_url="/login")
def categories(request):
    if request.method =="GET":
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
            "categories": categories,
        })

@login_required(login_url="/login")
def category(request, categoryid):
    if request.method =="GET":
        listing = Listing.objects.all().filter(category=categoryid,active=True)
        category = Category.objects.get(pk=categoryid)
        return render(request, "auctions/categorydetail.html", {
            "listing": listing,
            "category": category,
        })
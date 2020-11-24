from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionListing, Bid, Comment, Watchlist
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Max


class CloseBidForm(forms.Form):
    is_active = forms.BooleanField()
    listing_id = forms.IntegerField()


class BidForm(forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = [
            'user_id',
            'listing_id',
            'price'
        ]

        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }

class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = [
            'title', 
            'description',
            'photo',
            'price',
            'category'
            ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.URLInput(attrs={'class': 'form-control',
                'placeholder': f"Enter URL of photo"}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'})
        }
        

def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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

@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(
                user_id = request.user,
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                photo = form.cleaned_data["photo"],
                price = form.cleaned_data["price"],
                date = datetime.datetime.now(), 
                category = form.cleaned_data["category"]
            )
            new_listing.save()
        else:
            return HttpResponse('invalid input')
        return HttpResponseRedirect(reverse("index"))
    new_listing_form = NewListingForm()
    return render(request, "auctions/new_listing.html", {
        'new_listing_form': new_listing_form
    })

def display_listing(request, id):
    if request.user.id is None:
        return render(request, "auctions/error.html", {
            "message": f"Please register or log in to view item details."
        })

    listing = AuctionListing.objects.get(pk=id)
    watchlist = Watchlist.objects.filter(user_id=request.user).filter(listing_id=id)
    if request.method == "POST":
        if (Watchlist.objects.filter(user_id=request.user) and
                Watchlist.objects.filter(listing_id=listing.id)):
            Watchlist.objects.filter(user_id=request.user).filter(listing_id=listing.id).delete()
        else:
            watch_listing = Watchlist(
                user_id = request.user,
                listing_id = listing
            ) 
            watch_listing.save()
    # get highest bidder
    if Bid.objects.filter(listing_id=id):
        max_bid = Bid.objects.filter(listing_id=id).aggregate(Max('price'))['price__max']
        high_bid = Bid.objects.filter(listing_id=id).filter(price=max_bid)
        high_bid_user = high_bid[0].user_id.id
    else:
        high_bid = None
        high_bid_user = None
    bid_form = BidForm()
    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "watchlist": watchlist,
        "bid_form": bid_form,
        "high_bid": high_bid,
        "high_bid_user": high_bid_user
    })

@login_required
def bid(request, id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            price = float(AuctionListing.objects.get(
                id=form.cleaned_data["listing_id"].id).price)
            if Bid.objects.filter(listing_id=id):
                max_bid = float(max([bid.price for bid in Bid.objects.filter(
                listing_id=id)]))
            else:
                max_bid = price
            if (form.cleaned_data["price"] <= price or 
                form.cleaned_data["price"] <= max_bid):
                return render(request, "auctions/error.html", {
                    "message": f"Bid too low. Go higher."
                })
            # enter bid 
            bid = Bid(
                user_id = form.cleaned_data["user_id"],
                listing_id = form.cleaned_data["listing_id"],
                price = form.cleaned_data["price"]
            )
            bid.save()
            # update price on listing to reflect highest bid
            listing = AuctionListing.objects.get(id=id)
            listing.price = form.cleaned_data["price"]
            listing.save()
        else:
            return render(request, "auctions/error.html", {
                "message": f"Please enter valid bid."
            })
    return render(request, "auctions/confirmation.html", {
                "message": f"Your bid has been entered. You will be notified in the event of an offer. Thank you."
            })

def close(request, id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(id=id)
        user = User.objects.get(id=request.POST['highest_bidder'])
        listing.is_active = False
        listing.highest_bidder = user
        listing.save()
        return HttpResponseRedirect(reverse("display_listing", args=[id]))
    return render(request, "auctions/error.html", {
        "message": f"Something went wrong."
    })

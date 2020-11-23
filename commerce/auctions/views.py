from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionListing, Bid, Comment, Watchlist
import datetime


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
            'photo': forms.URLInput(attrs={'class': 'form-control'}),
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
        
    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "watchlist": watchlist
    })


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from decimal import Decimal  
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import Listings, Bids , Comments, Category,User



def index(request):
    listings = Listings.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


def listings(request):
    if request.method == 'GET':
        categoryes = Category.objects.all()
        return render(request, "auctions/listings.html" ,{
            "category" : categoryes
        })
    
def add_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        Description = request.POST['description']
        Bid_Amount = request.POST['starting_bid']
        Image = request.POST['url']
        category_id = request.POST['category']

        Category_data = get_object_or_404(Category, id=category_id)
        all_listing = Listings(
            title=title,
            description=Description,
            starting_bid = float(Bid_Amount),
            image_url = Image,
            owner=request.user,
            category = Category_data,
            is_active = True,
        )
        all_listing.save()
        return HttpResponseRedirect(reverse("index"))


def Particularlistingspage(request, listing_id):
    particularlist = get_object_or_404(Listings, id=listing_id, is_active=True)
    if request.method == "POST":
        action = request.POST.get("action", None)

        if action == "bid":
            bid_amountstr = request.POST.get("bid", None)
            if bid_amountstr:
                try:
                    bid_amount = Decimal(bid_amountstr)
                    if bid_amount > particularlist.starting_bid:
                        Bids.objects.create(
                            listing=particularlist,
                            bidder=request.user,
                            bid_amount=bid_amount
                        )
                        particularlist.starting_bid = bid_amount
                        particularlist.save()
                        messages.success(request, "Your bid has been placed successfully!")
                    else:
                        messages.success(request, "Your bid has been placed successfully!")

                except Decimal.InvalidOperation:
                    messages.error(request, "Invalid bid amount. Please enter a valid number.")
            else:
                messages.error(request, "Bid amount is required.")    
            
        elif action == "comment":
            user_comment = request.POST.get("comment", None)
            if user_comment:
                Comments.objects.create(
                    listing=particularlist,
                    commenter = request.user,
                    content = user_comment
                )
                messages.success(request, "Your Comment Have Been Added! ")
            else:
                messages.error(request, "Comment cannot be empty.")


    return render (request , "auctions/ParticualrListingPage.html", {
        "particularlist" : particularlist,
        "bids" : Bids.objects.filter(listing=particularlist),
        "comments": Comments.objects.filter(listing=particularlist)
    })


def Categories(request):
    categories = Category.objects.prefetch_related('listings')
    return render(request, "auctions/Categories.html",{
        "categories" : categories
    })


def Watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        particularlist = get_object_or_404(Listings, id=listing_id)

        if particularlist.watchlist.filter(id=request.user.id).exists():
            particularlist.watchlist.remove(request.user)
            messages.success(request, "Removed from your Watchlist.")
        else:
            particularlist.watchlist.add(request.user)
            messages.success(request, "Added to your Watchlist.")

    watchlist_items = request.user.watchlist.all()
    return render(request , "auctions/Watchlist.html", {
        "watchlist_items" : watchlist_items
    })
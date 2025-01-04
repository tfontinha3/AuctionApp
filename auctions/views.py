import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Listing, Bid, Watchlist, Comment
from .forms import ListingForm, CommentForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def listing_item(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    min_bid = listing.current_bid + 1
    comments = Comment.objects.filter(listing=listing).order_by('-date')  # Fetch comments for the listing

    is_in_watchlist = False
    if request.user.is_authenticated:
        watchlist, _ = Watchlist.objects.get_or_create(user=request.user)
        if listing in watchlist.listings.all():
            is_in_watchlist = True

    # Handle comment submission
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.date = timezone.now()
            comment.save()
            return redirect('listing_item', listing_id=listing.id)
    else:
        comment_form = CommentForm()

    return render(request, "auctions/listing_item.html", {
        "listing": listing,
        "min_bid": min_bid,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,  # Pass comments to the template
        "comment_form": comment_form  # Pass the comment form to the template
    })

def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # Create a new listing object, but don't save to the database yet
            listing = form.save(commit=False)
            
            # Set the additional fields
            listing.user = request.user  # Set the user to the currently logged-in user
            listing.current_bid = listing.starting_bid  # Set current_bid to starting_bid
            listing.bid_count = 0  # Set bid_count to 0
            listing.date = timezone.localtime(timezone.now())  # Set the date to the current date and time
            listing.active = True  # Set the listing to active
            
            # Now save the listing to the database
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))  # Redirect to the index page or wherever you want
    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {
        "form": form
    })

def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if not listing.active:
        messages.error(request, 'The auction is closed. Bidding is not allowed.')
        return redirect('listing_item', listing_id=listing.id)

    if request.method == "POST":
        bid_amount = int(request.POST.get('bid_amount'))

        if bid_amount > listing.current_bid:
            listing.current_bid = bid_amount
            listing.bid_count += 1
            listing.save()

            # Create a new bid entry
            Bid.objects.create(user=request.user, listing=listing, amount=bid_amount)

            messages.success(request, 'Your bid was successful!')
        else:
            messages.error(request, 'Your bid must be higher than the current bid.')

    return redirect('listing_item', listing_id=listing.id)


@login_required
def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all()
    })

@login_required
def watchlist_count(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    count = watchlist.listings.count()
    return JsonResponse({"count": count})

@login_required
def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    if listing in watchlist.listings.all():
        watchlist.listings.remove(listing)
        messages.success(request, 'Removed from your watchlist.')
    else:
        watchlist.listings.add(listing)
        messages.success(request, 'Added to your watchlist.')

    return redirect('listing_item', listing_id=listing.id)

def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    
    if request.user != listing.user:
        messages.error(request, "You do not have permission to close this auction.")
        return redirect('listing_item', listing_id=listing.id)

    highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

    if highest_bid:
        listing.winner = highest_bid.user
    listing.active = False  # Set the listing to inactive
    listing.save()

    messages.success(request, f"The auction has been closed. The winner is {listing.winner} with a bid of {highest_bid}$")
    return redirect('listing_item', listing_id=listing.id)

def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, active=True)
    return render(request, "auctions/categories_listings.html", {
        "category_name": category_name,
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

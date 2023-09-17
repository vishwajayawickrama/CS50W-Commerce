from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .forms import CreateListForm, CreateComments
from .models import User, Listings, Comments, Bids, WatchList


def index(request):
    all_listings = Listings.objects.all()
    return render(request, "auctions/index.html", {"objects": all_listings})


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
    
def createListing(request):
    if request.method == "POST":
        form =CreateListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            imageUrl = form.cleaned_data["imageUrl"]
            price = form.cleaned_data["price"]
            owner = request.user
            
            new_listing = Listings(title=title, description=description, imageUrl=imageUrl, price=price, owner=owner)
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListForm() 
    return render(request, "auctions/createlisting.html", {"form": form})

def listing(request, id):
    if request.method == "POST":
        comment = CreateComments(request.POST)
        if comment.is_valid():
            owner = request.user
            item = Listings.objects.get(id=id)
            current_comment = comment.cleaned_data["comment"]
            
            new_comment = Comments(owner=owner, item=item, comment=current_comment)
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(id,))) 
           
    listing = Listings.objects.get(id=id)
    owner = User.objects.get(id=listing.owner_id)
    comments = CreateComments()
    all_comments = Comments.objects.filter(item=id)
    
    return render(request, "auctions/listing.html", {
        "objects": listing, 
        "owner": owner,
        "comments": comments,
        "all_comments": all_comments
        })
    
    
def watch(request, id):
    if request.method == "POST":
        owner = request.user
        item = Listings.objects.get(id=id)
        
        new_watchlist = WatchList(owner=owner, item=item)
        new_watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(id,))) 
    return HttpResponseRedirect(reverse("listing", args=(id,)))
        
        
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listings, Category


def index(request):
    return render(request, "auctions/index.html")


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

def creat_new_list(request):
    if request.method == 'POST':
        #get the data from creat lising page
        list_titleq = request.POST.get('title')
        list_descriptionq = request.POST.get('description')
        list_imageq = request.POST.get('ImageUrl')
        list_starting_bidq = request.POST.get('starting_bid')
        #catagory part
        list_categoryq = request.POST.get('category')
        print(f"{list_categoryq}")
        categpry_instance = Category.objects.get(catogory_name=list_categoryq)
        # save the data 
        new_Listing = Listings(
            list_title=list_titleq,
            list_description=list_descriptionq,
            list_starting_bid=list_starting_bidq,
            list_image=list_imageq,
            list_catagpry=categpry_instance,
            list_active=True
        )
        new_Listing.save()
        return render(request, "auctions/index.html")
    else:
        all_catagoreys = Category.objects.all()
        return render(request, "auctions/creatnewlist.html",{'all_catagoreys':all_catagoreys})
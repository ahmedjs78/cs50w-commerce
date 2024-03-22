from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,redirect
from django.urls import reverse
from django.db.models import Max
from .models import User,Listings, Category,Bid
from django.utils import timezone 




def index(request):
    all_active_lists = Listings.objects.filter(list_active=True)
    all_closed_lists = Listings.objects.filter(list_active=False)
    return render(request, "auctions/index.html",{'all_active_lists':all_active_lists,'all_closed_lists':all_closed_lists})


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
        current_user = request.user
        print(f"{current_user}")
        user_instance = User.objects.get(username= current_user)
        # get the data from creat lising page
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
            list_active=True,
            list_owner=user_instance
        )
        new_Listing.save()
        return redirect(reverse('index'))
    else:
        all_catagoreys = Category.objects.all()
        return render(request, "auctions/creatnewlist.html",{'all_catagoreys':all_catagoreys})
    # add the method to make the user save watch list based on the user name 
def addToWatchList(request):
    if request.method == 'POST':
        curentuser = request.user
        pk = request.POST.get('num')
        listInstanse = Listings.objects.get(pk=pk)
        listInstanse.list_watch_list.add(curentuser)
    return redirect(reverse('viewitem', kwargs={'pk': pk}))
#work on remove method 
def removeFromWatchList(request):
    currentuser = request.user
    pk = request.POST.get('num')
    print(f"{pk}")
    list_instance = Listings.objects.get(pk=pk)
    list_instance.list_watch_list.remove(currentuser)
    return redirect(reverse('viewitem', kwargs={'pk': pk}))

def view_item(request,pk):
    error = request.GET.get('error')
    current_list = Listings.objects.get(pk=pk)
    bidOnThisList = Bid.objects.filter(onList=current_list)
    maxe = bidOnThisList.aggregate(b=Max('bidamount'))['b']
    returnuser = Bid.objects.get(bidamount=maxe)
    
    return render(request, "auctions/view_item.html", {"current_list":current_list,'maxe':maxe,'error':error,'returnuser':returnuser})



def addBid(request):
    currentUser = request.user
    
    pk = request.POST.get('pk')
    list_instance = Listings.objects.get(pk=pk)
    allbids = Bid.objects.filter(onList=list_instance)
    bid = request.POST.get('bid_amount')
    x = int(bid)
    maxee = allbids.aggregate(b=Max('bidamount'))['b']
    print(f"{x}")
    if maxee > x :
        error = True
        return redirect(reverse('viewitem', kwargs={'pk': pk})+ f'?error={error}')
    else:
        newbid = Bid(
            user_name=currentUser,
            onList=list_instance,
            bidamount=bid
        )
        newbid.save()
        return redirect(reverse('viewitem', kwargs={'pk': pk}))
    
def closeList(request):
     pk = request.POST.get('num')
     print(f"{pk}")
     list_instance = Listings.objects.get(pk=pk)
     list_instance.list_active = False
     list_instance.save()
     return redirect(reverse('viewitem', kwargs={'pk': pk}))
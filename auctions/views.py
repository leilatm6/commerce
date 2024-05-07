from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Max
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "auctions/index.html", {
        "products": Products.objects.filter(active=True),
    })


@login_required
def createlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        try:
            category = Category.objects.get(pk=request.POST["category"])
        except ObjectDoesNotExist:
            category = None
        print(category)
        newproduct = Products(title=title, initialprice=price, description=description, datetime=timezone.now(),
                              category=category, imageurl=imageurl, creatoruser=request.user)
        newproduct.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createlisting.html", {
        'category': Category.objects.all()
    })


def list(request, listid):
    try:
        product = Products.objects.get(pk=listid)
    except Products.DoesNotExist:
        ###########################################
        raise Http404("Auction Listing does not exist")
    max_bid_price = product.initialprice
    max_bid = None
    if len(product.productbids.all()) > 0:
        max_bid_price = Bid.objects.filter(product=product).aggregate(
            maxbid=Max('price'))['maxbid']
        max_bid = Bid.objects.filter(price=max_bid_price).first()

    if request.method == "POST":
        newbidprice = int(request.POST["bidinput"])
        if newbidprice <= max_bid_price:
            return render(request, "auctions/list.html", {
                "product": product,
                "maxbid": max_bid,
                "msg": f"Your bid should be greater than {max_bid_price}"
            })
            return HttpResponse("Invalid request", status=400)
        newbid = Bid(price=newbidprice, product=product, user=request.user)
        newbid.save()

        max_bid = newbid
    return render(request, "auctions/list.html", {
        "product": product,
        "maxbid": max_bid
    })


@csrf_exempt
def closelist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productid = int(data.get('id'))
        try:
            product = Products.objects.get(pk=productid)
        except Products.DoesNotExist:
            ###########################################
            raise Http404("Auction Listing does not exist")
        print(product)
        product.active = False
        product.save()
        response_data = {'message': 'Data closed successfully'}
        return JsonResponse(response_data)
    else:
        # Handle other HTTP methods if needed
        # For simplicity, return a method not allowed response
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

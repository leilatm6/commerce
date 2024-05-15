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


def index(request, categoryid=None):
    headername = "Active Listing"
    if categoryid:
        try:
            category = Category.objects.get(pk=categoryid)
            products = category.products.all()
        except Category.DoesNotExist:
            # Handle the case where the category does not exist
            products = []
        headername = category.title
    else:
        products = Products.objects.filter(active=True)
        headername = "Active Listing"
    productset = [(product, Bid.objects.filter(product=product).aggregate(maxbid=Max('price'))['maxbid']
                   if len(product.productbids.all()) > 0 else product.initialprice) for product in products]
    return render(request, "auctions/index.html", {
        "products": productset,
        "headername": headername})


def has_watchlist_item(product, user):
    try:
        Watchlist.objects.get(user=user, product=product)
        return True
    except Watchlist.DoesNotExist:
        return False


@csrf_exempt
@login_required
def watchlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productid = int(data.get('id'))
        try:
            product = Products.objects.get(pk=productid)
        except product.DoesNotExist:
            ###############################
            raise Http404("Auction Listing does not exist")
        if has_watchlist_item(product, request.user):
            watchlist_item = Watchlist.objects.get(
                product=product, user=request.user)
            watchlist_item.delete()
            iswatchlist = False
        else:
            new_watchlist_item = Watchlist(product=product, user=request.user)
            new_watchlist_item.save()
            iswatchlist = True

        response_data = {'message': 'updated successfully',
                         'iswatchlist': iswatchlist}
        return JsonResponse(response_data)
    else:
        userwatchlist = Watchlist.objects.filter(user=request.user)
        if userwatchlist:
            productset = [(watchlist.product, Bid.objects.filter(product=watchlist.product).aggregate(maxbid=Max('price'))['maxbid']
                           if len(watchlist.product.productbids.all()) > 0 else watchlist.product.initialprice) for watchlist in userwatchlist]
            return render(request, "auctions/index.html", {
                "products": productset,
                "headername": "Your Watchlist"
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
    section = None
    max_bid_price = product.initialprice
    max_bid = None
    lenbids = len(product.productbids.all())
    if lenbids > 0:
        max_bid_price = Bid.objects.filter(product=product).aggregate(
            maxbid=Max('price'))['maxbid']
        max_bid = Bid.objects.filter(price=max_bid_price).first()
    watchlist = False
    if request.user.is_authenticated:
        if has_watchlist_item(product, request.user):
            watchlist = True
    comments = Comments.objects.filter(
        product=product).order_by('datetime')
    if request.method == "POST":
        section = 'bid'
        newbidprice = int(request.POST["bidinput"])
        if newbidprice < max_bid_price or (newbidprice == max_bid_price and lenbids > 0):
            return render(request, "auctions/list.html", {
                "product": product,
                "maxbid": max_bid,
                "msg": f"Your bid should be greater than {max_bid_price}",
                "iswatchlist": watchlist,
                "section": section,
                "comments": comments
            })
            return HttpResponse("Invalid request", status=400)
        newbid = Bid(price=newbidprice, product=product, user=request.user)
        newbid.save()
        max_bid = newbid
    print(max_bid.user)
    print(product.active)
    return render(request, "auctions/list.html", {
        "product": product,
        "maxbid": max_bid,
        "iswatchlist": watchlist,
        "section": section,
        "comments": comments
    })


@csrf_exempt
@login_required
def createcomment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        textarea = data.get('textarea')
        productid = data.get('id')
        print(textarea)
        print(productid)
        try:
            product = Products.objects.get(pk=productid)
        except Products.DoesNotExist:
            ###########################################
            raise Http404("Auction Listing does not exist")
        new_comment = Comments(
            user=request.user, product=product, text=textarea, datetime=timezone.now())
        new_comment.save()
        response_data = {'message': 'comment added successfully'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all(),
    })


@csrf_exempt
@login_required
def closelist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productid = int(data.get('id'))
        try:
            product = Products.objects.get(pk=productid)
        except Products.DoesNotExist:
            ###########################################
            raise Http404("Auction Listing does not exist")
        if request.user != product.creatoruser:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
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

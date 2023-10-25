from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Events,Tickets
from django.http import JsonResponse
import json
from datetime import datetime

def index(request):
    return render(request, "events/index.html",{
        "events": Events.objects.order_by("-date").all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"] 
        password = request.POST["password"] 
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user) 
            return HttpResponseRedirect(reverse("index")) 
          
        else:
            return render(request, "events/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "events/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "events/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            username = request.POST["username"] 
            email = request.POST["email"] 
            user = User.objects.create_user(username, email, password) 
            user.save()
        except IntegrityError:
            return render(request, "events/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "events/register.html")
    
def event(request,event_id):
    if request.method=='GET':
        event=Events.objects.get(pk=event_id)
        if  request.user.is_authenticated:
            return render(request,'events/event.html',{
                'event':event,
                "color": "red" if event in request.user.wishlist.all() else "black",
                "available_tickets": event.tickets
            })
        else:
            return render(request,'events/event.html',{
                'event':event,
                "color": "black",
                "available_tickets": event.tickets
            })
    


@login_required
def wishlist(request):
    if request.method=="GET":
        return render(request, "events/wishlist.html",{
            "wishlists": request.user.wishlist.all()
        })
    elif request.method=="POST":
        data = json.loads(request.body)
        event_id = data.get("id")
        event = Events.objects.get(id=event_id)
        existing_wishlist_item = request.user.wishlist.filter(id=event_id).first()
        if existing_wishlist_item:
    # Item already exists in the wishlist, so remove it
            request.user.wishlist.remove(event)
            return JsonResponse({"message": "Removed from wishlist"}, status=201)
        # Item doesn't exist in the wishlist, so add it
        request.user.wishlist.add(event)
        return JsonResponse({"message": "Added to wishlist"}, status=201)
    else:
        return HttpResponse("Method not allowed")
    

@login_required
def orders(request):
    if request.method=="GET":
        orders=request.user.tickets.all()
        orders=orders.order_by("-event__date").all()
        return JsonResponse([order.serialize() for order in orders],safe=False)

    elif request.method=="POST":
        data = json.loads(request.body)
        event_id = data.get("id")
        event = Events.objects.get(id=event_id)
        quantity = data.get("quantity")
        if event.tickets < quantity:
            return JsonResponse({"message": "Not enough tickets"}, status=400)
        event.tickets -= quantity
        event.save()
        existing_order = request.user.tickets.filter(event=event).first()
        if existing_order:
            existing_order.quantity += quantity
            existing_order.save()
            return JsonResponse({"message": "Updated order"}, status=201)
        order = Tickets(user=request.user, event=event, quantity=quantity)
        order.save()
        return JsonResponse({"message": "Order placed"}, status=201)
    else:
        return HttpResponse("Method not allowed")
    


def get_events(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        selected_date = data.get("date")
        mday,month, date, year = selected_date.split(" ")
        selected_date = f"{month}/{date}/{year}"
        # Convert the selected_date to a datetime object
        events=Events.objects.all()
        actual_events=[]
        for event in events:
            if event.date_formatted()==selected_date:
                actual_events.append(event)
        # Extract the date part and filter events based on the date

        # Serialize the events and return as JSON
        event_data = [event.serialize() for event in actual_events]
        
        return JsonResponse({   'events':event_data,
                             'message':'success',
                             }, safe=False, status=200)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method=="GET":
            return render(request,"events/create.html")
        elif request.method=="POST":
            title=request.POST["title"]
            description=request.POST["description"]
            date=request.POST["date"]
            location=request.POST["location"]
            image=request.FILES["image"]
            club=request.POST["club"]
            ticket_price=request.POST["ticket_price"]
            category=request.POST["category"]
            duration=request.POST["duration"]
            tickets=request.POST["tickets"]
            event=Events(title=title,description=description,date=date,location=location,image=image,club=club,ticket_price=ticket_price,duration=duration,tickets=tickets)
            event.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Method not allowed")
        

def categories(request):
    if request.method=="GET":
        return render(request,"events/categories.html",{
            "categories":Events.objects.values('category').distinct()
        })
    else:
        return HttpResponse("Method not allowed")
    
def help(request):
    if request.method=="GET":
        return render(request,"events/help.html")
    else:
        return HttpResponse("Method not allowed")
    

@login_required
def account(request):
    if request.method=="GET":
        if request.content_type == 'application/json':
            return JsonResponse(request.user.serialize())
        else:
            return render(request, "events/account.html",{
                "User": request.user
            })
    

def search(request):
    if request.method=="POST":
        query=request.POST["query"]
        events=Events.objects.all()
        actual_events=[]
        for event in events:
            if query.lower() in event.title.lower() or query.lower() in event.description.lower() or query.lower() in event.club.lower():
                actual_events.append(event)
        return render(request,"events/search.html",{
            "events":actual_events
        })
    elif request.method=="GET":
        return HttpResponseRedirect(reverse("index"))
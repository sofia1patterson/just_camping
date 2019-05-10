from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Park, Campsite, Booking
from django.db.models import Count
import bcrypt
import re

def home(request):
    if 'user_id' not in request.session:
        return render(request, "project_app/home.html")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
        }
        return render(request, "project_app/home.html", context)

def about(request):
    if 'user_id' not in request.session:
        return render(request, "project_app/about.html")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
        }
        return render(request, "project_app/about.html", context)

def destinations(request):
    if 'user_id' not in request.session:
        return render(request, "project_app/destinations.html")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
        }
        return render(request, "project_app/destinations.html", context)

def lassen(request):
    if 'user_id' not in request.session:
        return render(request, "project_app/lassen.html")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
            'all_campsites' : Campsite.objects.all(),
        }
        return render(request, "project_app/lassen.html", context)

def butte(request):
    if 'user_id' not in request.session:
        context = {
            'this_campsite' : Campsite.objects.get(id=1),
        }
        return render(request, "project_app/butte.html", context)
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
            'this_campsite' : Campsite.objects.get(id=1),
            "lassen_id" : Park.objects.get(id=1),
        }
        return render(request, "project_app/butte.html", context)

def juniper(request):
    if 'user_id' not in request.session:
        context = {
            'this_campsite' : Campsite.objects.get(id=2),
        }
        return render(request, "project_app/juniper.html", context)
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
            'this_campsite' : Campsite.objects.get(id=2),
            "lassen_id" : Park.objects.get(id=1),
        }
        return render(request, "project_app/juniper.html", context)

def manzanita(request):
    return render(request, "project_app/manzanita.html")

def booking_login(request):
    id = request.POST['campsite_id']
    same_email = User.objects.filter(email = request.POST['l_email'])
    if len(same_email) != 1:
        messages.error(request,"Email/password incorrect")
        return redirect("/loginreg")
    if len(request.POST['l_email']) < 1:
        messages.error(request,"Email/password incorrect")
        return redirect("/loginreg")
    else:
        logged_user = User.objects.get(email=request.POST['l_email'])
        request.session['user_id'] = logged_user.id
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()): 
            return redirect(f"/booking/{id}")
        else:
            messages.error(request, "Email/password incorrect")
            return redirect("/loginreg")
        return redirect("/loginreg")

def booking_page(request, id):
    if 'user_id' not in request.session:
        return redirect("/destinations")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
            'this_campsite' : Campsite.objects.get(id=id),
        }
        return render(request, "project_app/booking.html", context)

def booking(request, id):
    if len(request.POST['first_name']) < 2:
        messages.error(request, "First name should be at least 2 characters")
        return redirect(f"/booking/{id}")
    if len(request.POST['last_name']) < 2:
        messages.error(request, "Last name should be at least 2 characters")
        return redirect(f"/booking/{id}")
    if len(request.POST['from']) < 10 or len(request.POST['to']) < 10:
        messages.error(request, "Please enter a valid date")
        return redirect(f"/booking/{id}")
    if len(request.POST['phone_number']) < 10:
        messages.error(request, "Invalid Phone Number")
        return redirect(f"/booking/{id}")
    if len(request.POST['number']) < 1 or len(request.POST['loop']) < 1:
        messages.error(request, "Please enter valid site")
        return redirect(f"/booking/{id}")
    if len(request.POST['nights']) < 1:
        messages.error(request, "Please enter number of nights")
        return redirect(f"/booking/{id}")
    else:
        this_campsite = Campsite.objects.get(id=id)
        request.session['from'] = request.POST['from']
        request.session['to'] = request.POST['to']
        request.session['quantity'] = int(request.POST['nights'])
        request.session['site_number'] = request.POST['number']
        request.session['site_loop'] = request.POST['loop']
        request.session['fname'] = request.POST['first_name']
        request.session['lname'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone_number']
        request.session['occupants'] = request.POST['occupants']
        request.session['vehicles'] = request.POST['vehicles']
        request.session['site_type'] = request.POST['site']
        request.session['price'] = float(this_campsite.nightly_rate)
        request.session['total_price'] = request.session['quantity'] * request.session['price']
        request.session['count'] = 1
        return redirect(f"/cart/{id}")

def cart(request,id):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user' : current_user,
        'this_campsite' : Campsite.objects.get(id=id),
    }
    return render(request, 'project_app/cart.html', context)

def loginreg_page(request):
    return render(request, "project_app/loginreg.html")
    

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/loginreg")
    else:
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = user.id
        print(user.password)
        return redirect("/destinations")

def login(request):
    same_email = User.objects.filter(email = request.POST['l_email'])
    if len(same_email) != 1:
        messages.error(request,"Email/password incorrect")
        return redirect("/loginreg")
    if len(request.POST['l_email']) < 1:
        messages.error(request,"Email/password incorrect")
        return redirect("/loginreg")
    else:
        logged_user = User.objects.get(email=request.POST['l_email'])
        request.session['user_id'] = logged_user.id
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()): 
            return redirect("/destinations")
        else:
            messages.error(request, "Email/password incorrect")
            return redirect("/loginreg")
        return redirect("/loginreg")

def user(request):
    if 'user_id' not in request.session:
        return redirect("/loginreg")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user' : current_user,
        }
        return render(request, "project_app/user_page.html", context)

def delete(request):
    del request.session['from']
    del request.session['to']
    del request.session['quantity']
    del request.session['site_number']
    del request.session['site_loop']
    del request.session['fname']
    del request.session['lname']
    del request.session['email']
    del request.session['phone']
    del request.session['occupants']
    del request.session['vehicles']
    del request.session['site_type']
    del request.session['price']
    del request.session['total_price']
    del request.session['count']
    return redirect("/destinations")

def logout(request):
    del request.session['user_id']
    return redirect("/")
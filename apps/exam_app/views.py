from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    return render(request, 'exam_app/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        
        taken_usernames = User.objects.filter(username = request.POST['username'])
        taken_username = taken_usernames.first()
        if taken_username > 1:
            messages.error(request, "Username has already been taken", extra_tags='username')
            return redirect ('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pw)
            request.session['name'] = request.POST['name']
            request.session['id'] = User.objects.get(username = request.POST['username']).id
            return redirect('/dashboard')
    
def login(request):
    users = User.objects.filter(username = request.POST['username'])
    if request.method == "POST":
        if len(users) < 1:
            messages.error(request, 'Username has not been registered', extra_tags='username')
            return redirect('/')
        if len(users) > 0:
            user = users.first()
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['name'] = user.name
                request.session['id'] = user.id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Invalid password', extra_tags='password')
                return redirect('/')
        else:  
            messages.error(request, "Login failed", extra_tags='login')
            return redirect('/')

def dashboard(request):
    my_wishes = list(Wishlist.objects.filter(creator_id = request.session['id']))
    other_wishes = list(Wishlist.objects.exclude(creator_id = request.session['id']))
    remove_list = list()

    for wish in other_wishes:
        for item in wish.wishlists.all():
            if item.name == request.session['name']:
                my_wishes.append(wish)
                remove_list.append(wish)
    
    for wish in remove_list:
        other_wishes.remove(wish)

    context = {
        "my_wishes": my_wishes,
        "other_wishes": other_wishes
    }
    return render(request, 'exam_app/dashboard.html', context)

def add_item(request):
    return render(request, 'exam_app/add_item.html')

def create(request):
    if request.method == "POST":
        if len(request.POST['item']) < 4:
            messages.error(request, "Item/Product should be more than 3 characters", extra_tags='item')
            return redirect('/add_item')
        else:
            user = User.objects.get(id = request.session['id'])
            Wishlist.objects.create(item = request.POST['item'], creator = user)
            return redirect('/dashboard')

def wish_item(request, wish_id):
    context = {
        "wishes": Wishlist.objects.get(id = wish_id),
    }
    return render(request, 'exam_app/wish_item.html', context)

def add_wish(request, wish_id):
    wish = Wishlist.objects.get(id = wish_id)
    user = User.objects.get(id = request.session['id'])
    wish.wishlists.add(user)
    print wish
    return redirect('/dashboard')

def remove(request, wish_id):
    wish = Wishlist.objects.get(id = wish_id)
    user = User.objects.get(id = request.session['id'])
    wish.wishlists.remove(user)
    return redirect('/dashboard')

def remove_self(request, wish_id):
    Wishlist.objects.get(id = wish_id).delete()
    return redirect('/dashboard')

def logout(request):
    request.session['id'] = 0
    return redirect('/')
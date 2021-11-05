from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from time import sleep
from django.contrib.auth.models import User



# Create your views here.



# @login_required(login_url="login")
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'No! Account Founded')
    context = {

    }
    return render(request, "login.html", context)



# @login_required(login_url="login")
def signup_page(request):

    sign_up = True
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        
        try: 
            match_email = User.objects.get(email=email)
        except:
            match_email = None
        
        try: 
            match_username = User.objects.get(username=username)
        except:
            match_username = None


        if password!=password2:
            messages.error(request, 'Password Not Matching')
        
        if match_email != None:
            messages.error(request, 'Please Use a Different Email')

        if match_username != None:
            # sleep(1)
            messages.error(request, 'Please Use a Different Username')
            return redirect("signup-page")


        user = User.objects.create_user(username.lower(), email, password)
        user.first_name = f_name
        user.last_name = l_name
        user.save()
        user_details = User_detail.objects.create(user=user)
        user_details.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            dj_login(request, user)

        

    # f = UserCreationForm()
    # if request.method == "POST":
    #     f = UserCreationForm(request.POST)
    #     if f.is_valid():
    #         f.save()
    #         # login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Try a Different Username')

    context = {
    "sign_up": sign_up,
    # "forms":f,
    }


        # user = authenticate(username=username, password=password)
    
    return render(request, "login.html", context)


# @login_required(login_url="login")
def logout_page(request):
    dj_logout(request)
    context = {

    }
    return redirect('login-page')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) 
    ).order_by('created').reverse()
    topics = Topic.objects.all()[0:5]
    room_count = Room.objects.all().count()
    activity_logs = Message.objects.all().order_by('created').reverse()[:10]
    context = {
        "rooms":rooms,
        "topics":topics,
        "room_count":room_count,
        "activity_logs":activity_logs,
    }

    return render(request, 'home.html', context)


@login_required(login_url="login-page")
def create_room(request):
    if request.method == "POST":
        topic_name = request.POST.get('topic_name')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
        host = request.user,
        name = request.POST.get('room_name'),
        topic =topic,
        )
        return redirect("home")
    topics = Topic.objects.all()
    context = {
        "topics":topics
    }
    return render(request, "create-room.html", context)


# @login_required(login_url="login-page")
def roompage(request,pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )
        room.participants.add(request.user)

        return redirect("room-page", pk=room.id)
    context = {
        "room":room,
        "messages":messages,
        "participants":participants,
    }

    return render(request, "room.html", context)



# @login_required(login_url="login-page")
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    context = {
        "room":room,
        "topics":topics
    }
    if request.method == "POST":
        name = request.POST.get('room_name')
        topic_name = request.POST.get('topic_name')
        room.topic, created = Topic.objects.get_or_create(name=topic_name)  
        room.name = name
        room.save()
        return redirect("room-page", pk=room.id)


    return render(request, "create-room.html", context)




def profile_page(request,pk):
    profile = User.objects.get(id=pk)
    activity_logs = Message.objects.all().order_by('created').reverse()
    topics = Topic.objects.all()[0:5]
    room_count = Room.objects.all().count()
    rooms = profile.room_set.all()
    context = {
        "topics":topics,
        "room_count":room_count,
        "profile":profile,
        "activity_logs":activity_logs,
        "rooms":rooms
    }
    return render(request, "profile.html", context)

def edit_user(request, pk):
    editing_user = User.objects.get(id=pk)
    editing_user_details = User_detail.objects.get(user=editing_user)
    if (request.user) != editing_user:
        return redirect("home")
    else:
        if request.method == "POST":
            try:
                editing_user_details.avatar = request.FILES["avatar"]
            except:
                pass
            editing_user_details.bio = request.POST.get("user_bio")
            editing_user.username = request.POST.get("username")
            editing_user.email = request.POST.get("email")

            editing_user.save()
            editing_user_details.save()

            return redirect(request.META.get('HTTP_REFERER'))


# name = request.POST.get('room_name')
#         topic_name = request.POST.get('topic_name')
#         room.topic, created = Topic.objects.get_or_create(name=topic_name)  
#         room.name = name
#         room.save()
    context = {
        "editing_user":editing_user
    }

    return render(request, "edit-user.html", context)

def delete_message(request, pk):
    del_message = Message.objects.get(id=pk)
    if request.user != del_message.user:
        return redirect("home")
    if request.method == "POST":
        del_message.delete()
        return redirect("home")
    context = {
        "obj":del_message
    }
    return render(request, "delete.html", context)

def delete_room(request, pk):
    del_room = Room.objects.get(id=pk)
    if request.user != del_room.host:
        return redirect("home")
    if request.method == "POST":
        del_room.delete()
        return redirect("home")
    context = {
        "obj":del_room
    }
    return render(request, "delete.html", context)

def topic_page(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) 
    ).order_by('created').reverse()

    topics = Topic.objects.all()
    room_count = Room.objects.all().count()
    context = {
        "topics":topics,
        "room_count":room_count,

        }
    return render(request, "topics.html", context)
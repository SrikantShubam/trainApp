from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import trains, person


def index(request):
    lis = trains.objects.all()
    return render(request, './index.html', {"lis": lis})


def loginform(request):
    return render(request, './login.html')


def login(request):
    u = request.POST
    user = authenticate(request, username=u['name'], password=u['password'])
    if user is not None:
        auth_login(request, user)
        context = {
            'msg': "Login Successsful"
        }
    else:
        context = {
            'msg': "Error User is not registered/invalid"
        }
    return render(request, './error.html', context)


def registerform(request):
    return render(request, './register.html')


def register(request):
    user = request.POST
    u = User.objects.create_user(user['name'], user['email'], user['password'])
    u.save()
    context = {
        'msg': "Registeration Successsful"
    }
    return render(request, './error.html', context)


def logout(request):
    auth_logout(request)

    context = {
        'msg': "Logout Successful"
    }
    return render(request, './error.html', context)






temp={}
def book(request):
    global temp
    if request.user.is_authenticated:
        t = trains.objects.filter(
            source=request.POST['source'], destination=request.POST['destination'])
        if len(t):
            temp['name']=request.POST['name']
            temp['age']=request.POST['age']
            temp['gender']=request.POST['gender']

            return render(request, './trainsavailable.html', {'trains': t})
        else:
            return render(request, './error.html', {'msg': "Not Found"})
    else:
        return render(request, './error.html', {'msg': "Not a valid user. Please Login to continue"})


def booking(request, train_id):
    tt = trains.objects.get(pk=train_id)
    if tt.seats_available == 0:
        return render(request, './error.html', {'msg': "Seats full"})
    tt.seats_available -= 1

    p = person(train=tt, name=temp['name'], email=request.user.email,age=temp['age'],gender=temp['gender'])
    p.save()
    tt.save()

    return render(request, './error.html', {'msg': "Booked Successfully...Price to be paid is "+str(tt.price)})


def bookform(request):
    t = trains.objects.all()
    sources = []
    destinations = []
    for i in t:
        sources.append(i.source)
        destinations.append(i.destination)
    sources = list(set(sources))
    destinations = list(set(destinations))

    if request.user.is_authenticated:
        return render(request, './booking.html', {'sources': sources, 'destinations':destinations})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})

def addtrain(request):
        source=request.POST['source'], destination=request.POST['destination']
        print(source)

def mybooking(request):
    if request.user.is_authenticated:
        p = person.objects.filter(email=request.user.email)
        return render(request, './mybooking.html', {'persons': p})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})

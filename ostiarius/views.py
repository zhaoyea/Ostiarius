from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import *
from .models import *
from .serializers import ItemSerializer


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        alerts = Alert.objects.all()
        items = Item.objects.all()
        item_stolen = Alert.objects.all().count()
        item_present = Item.objects.filter(present=0).count()
        item_maintenance = Item.objects.filter(maintenance=1).count()
        return render(request, 'ostiarius/index.html', {
            'alerts': alerts,
            'items': items,
            'item_stolen': item_stolen,
            'item_present': item_present,
            'item_maintenance': item_maintenance,
        })


def detail(request, alert_id):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        details = get_object_or_404(Alert, pk=alert_id)
        return render(request, 'ostiarius/details.html', {'details': details})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'ostiarius/index.html')
            else:
                return render(request, 'ostiarius/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'ostiarius/login.html', {'error_message': 'Invalid Username or Password'})
    return render(request, 'ostiarius/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'ostiarius/login.html', context)


def assets(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        asset_ids = []
        for items in Item.objects.all():
            asset_ids.append(items.pk)
        assets = Item.objects.filter(pk__in=asset_ids)
    return render(request, 'ostiarius/assets.html', {'assets': assets})


@api_view(['GET', 'POST'])
def asset_list(request):
    if request.method == 'GET':
        asset = Item.objects.all()
        serializer = ItemSerializer(asset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def control(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        return render(request, 'ostiarius/control.html')

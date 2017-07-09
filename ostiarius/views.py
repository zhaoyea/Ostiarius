from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import *
import json
from .models import *
from .serializers import *
from rest_framework.renderers import JSONRenderer


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        alerts = Alert.objects.all()
        item_stolen = Alert.objects.all().count()
        item_present = Item.objects.filter(present=0).count()
        return render(request, 'ostiarius/index.html', {
            'alerts': alerts,
            'maintenance': maintenance,
            'item_stolen': item_stolen,
            'item_present': item_present,
        })


def assets(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        items = Item.objects.all()
        return render(request, 'ostiarius/assets.html', {
            'items': items,
        })


def maintenancePage(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        items = Item.objects.all()
        maintenance = Maintenance.objects.all()
        return render(request, 'ostiarius/maintenance.html', {
            'items': items,
            'maintenance': maintenance,
        })


def alertPage(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        items = Item.objects.all()
        alerts = Alert.objects.all()
        return render(request, 'ostiarius/alert.html', {
            'items': items,
            'alerts': alerts,
        })


def blank_table(request):
    asset = Item.objects.all()
    serializer = ItemSerializer(asset, many=True)
    data = JSONRenderer().render(serializer.data)
    output = json.dumps(json.loads(data), indent=4)
    return render(request, 'ostiarius/blank-tables.html', {'output': output})


def present(request, present_id):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        item_present = Item.objects.filter(present=0)
        details = get_object_or_404(Alert, pk=present_id)
        return render(request, 'ostiarius/detail.html', {
            'details': details,
            'item_present': item_present,
        })


def alert(request, alert_id):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        item_stolen = Alert.objects.all()
        details = get_object_or_404(Alert, pk=alert_id)
        return render(request, 'ostiarius/detail.html', {
            'details': details,
            'item_stolen': item_stolen,
        })


def maintenance(request, maintenance_id):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        not_return = Maintenance.objects.filter(returnDate=None)
        details = get_object_or_404(Alert, pk=maintenance_id)
        return render(request, 'ostiarius/detail.html', {
            'details': details,
            'not_return': not_return,
        })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('ostiarius:index')
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
    return render(request, 'music/login.html', context)


def update_items(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        item_id = request.POST['item_id']
        new_item = Item.objects.get(id=item_id)
        new_item_name = request.POST['item_name']
        new_present = request.POST['present']
        new_item.present = new_present
        new_item.item_name = new_item_name
        new_item.save()
        return redirect('ostiarius:assets')


def update_maintenance(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        maintain_item_id = request.POST['maintain_item_id']
        if Maintenance.objects.get(item_id=maintain_item_id):
            return render(request, 'ostiarius/assets.html', {'msg': "Item already under maintenance"})
        maintainDate = request.POST['maintainDate']
        return redirect('ostiarius:assets')


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

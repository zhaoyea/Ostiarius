from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import *
import re, json
from datetime import date
from .models import *
from .serializers import *
import requests


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        alerts = Alert.objects.filter(date=date.today())
        item_stolen = Alert.objects.all().count()
        item_present = Item.objects.filter(present=0).count()
        item_maintenance = Item.objects.filter(maintenance_mode=1).count()
        maintain_overdue = Maintenance.objects.filter(return_date__lt=date.today())

        jan = Alert.objects.filter(date__month='01')
        feb = Alert.objects.filter(date__month='02')
        mar = Alert.objects.filter(date__month='03')
        april = Alert.objects.filter(date__month='04')
        may = Alert.objects.filter(date__month='05')
        june = Alert.objects.filter(date__month='06')
        july = Alert.objects.filter(date__month='07')
        aug = Alert.objects.filter(date__month='08')
        sep = Alert.objects.filter(date__month='09')
        oct = Alert.objects.filter(date__month='10')
        nov = Alert.objects.filter(date__month='11')
        dec = Alert.objects.filter(date__month='12')

        alert_data = [jan.count(), feb.count(), mar.count(), april.count(), may.count(), june.count(), july.count(),
                      aug.count(), sep.count(), oct.count(), nov.count(), dec.count()]

        data = {
            'alerts': alerts,
            'item_stolen': item_stolen,
            'item_present': item_present,
            'item_maintenance': item_maintenance,
            'maintain_overdue': maintain_overdue,
            'alert_data': alert_data,
        }
        return render(request, 'ostiarius/index.html', data)


def assets(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        items = Item.objects.all()
        maintenance = Maintenance.objects.all()
        return render(request, 'ostiarius/assets.html', {
            'items': items,
            'maintenance': maintenance,
        })


def maintenancePage(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        items = Item.objects.all()
        maintenance = Maintenance.objects.all()
        today = date.today()
        return render(request, 'ostiarius/maintenance.html', {
            'items': items,
            'maintenance': maintenance,
            'today': today,
        })


def present(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        item_present = Item.objects.filter(present=0)
        return render(request, 'ostiarius/detail.html', {
            'item_present': item_present,
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


def alert(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        alerts = Alert.objects.filter(date=date.today())
        return render(request, 'ostiarius/detail.html', {
            'alerts': alerts,
        })


def maintenance(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        maintenance = Maintenance.objects.filter(status=1)
        return render(request, 'ostiarius/detail.html', {
            'maintenance': maintenance,
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
    return render(request, 'ostiarius/login.html', context)


def console(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        return render(request, 'ostiarius/console.html')


def settings(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        return render(request, 'ostiarius/settings.html')


def add_items(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        new_asset_no = request.POST['new_asset_no']
        new_item_name = request.POST['new_item_name']
        new_item = Item(asset_no=new_asset_no, item_name=new_item_name)
        new_item.save()
        print("New Asset:" + new_asset_no + " - " + new_item_name + " added to Asset Table")
        return redirect('ostiarius:assets')


def delete_items(request, item_id):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        item = Item.objects.get(pk=item_id)
        item.delete()
        return redirect('ostiarius:assets')


def update_items(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        item_id = request.POST['item_id']
        new_item = Item.objects.get(id=item_id)
        new_item_name = request.POST['item_name']
        if not new_item_name:
            error_msg = "Item name cannot be null"
            print(error_msg)
            return redirect('ostiarius:assets')
        else:
            new_item.item_name = new_item_name
            new_item.save()
            success_msg = "Item name change to " + new_item_name
            print(success_msg)
            return redirect('ostiarius:assets')


def new_maintenance(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        itemStr = request.POST['maintain_asset_no']
        maintain_asset_no = re.search('(.+)[\s?][\^-].+', itemStr).group(1)
        print("Maintenance Asset No ---" + maintain_asset_no)
        item = Item.objects.get(asset_no=maintain_asset_no)
        staff_name = request.POST['staff_name']
        maintain_date = request.POST['maintain_date']
        return_date = request.POST['return_date']

        if Maintenance.objects.filter(asset_no=maintain_asset_no) and Maintenance.objects.filter(status=1):
            print("Item already under maintenance")
            return redirect('ostiarius:maintenancePage')

        else:
            maintain = Maintenance(asset_no=maintain_asset_no, staff_name=staff_name, date=maintain_date,
                                   return_date=return_date, item_id=item.id)
            maintain.save()
            item.maintenance_mode = True
            item.present = False
            item.save()
            return redirect('ostiarius:maintenancePage')


def update_maintenance(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html', {'error_message': 'Please login first'})
    else:
        maintain_item_id = request.POST['maintain_item_id']
        new_item = Item.objects.get(id=maintain_item_id)
        new_maintain = Maintenance.objects.get(item_id=maintain_item_id)
        maintain_status = request.POST['maintain_status']
        maintain_staff_name = request.POST['staff_name']
        maintain_date = request.POST['maintainDate']

        if new_maintain.status:
            new_maintain.status = maintain_status
            new_maintain.staff_name = maintain_staff_name
            new_maintain.date = maintain_date
            new_maintain.save()
            new_item.maintenance_mode = maintain_status
            new_item.present = True
            new_item.save()
            print("Maintenance table updated")
            return redirect('ostiarius:maintenancePage')
        else:
            new_maintain.status = maintain_status
            new_maintain.staff_name = maintain_staff_name
            new_maintain.date = maintain_date
            new_maintain.save()
            new_item.maintenance_mode = maintain_status
            new_item.present = False
            new_item.save()
            print("Maintenance table updated")
            return redirect('ostiarius:maintenancePage')


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


def jsonData(request):
    asset = Item.objects.all()
    serializer = ItemSerializer(asset, many=True)
    return JsonResponse(serializer.data, safe=False)


def piGET(request):
    res = requests.get("http://128.199.75.229/status.php")
    return JsonResponse(res.json(), safe=False)


def GETrequest(request):
    res = requests.get("http://128.199.75.229/items.php")
    return JsonResponse(res.json(), safe=False)


def POSTassets(request):
    if not request.user.is_authenticated():
        return render(request, 'ostiarius/login.html')
    else:
        res = requests.get("http://128.199.75.229/items.php")
        data = res.json()
        for key, value in data.items():
            for item in value:
                if not Item.objects.filter(asset_no=item['asset_no']):
                    serializer = ItemSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()

    return redirect('ostiarius:assets')


def blank_table(request):
    return render(request, 'ostiarius/blank-tables.html')

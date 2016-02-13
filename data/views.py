from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import simplejson
from .models import Item
import requests

# Create your views here.

def index(request):
    items = Item.objects.filter(selected = True)
    renderitems = []
    # print "found " + str(len(items)) + " items"
    if len(items) != 0:
        idlist = ""
        for item in items:
            idlist += str(item.item_api_id) + ","
        idlist = idlist[:-1]
        updateresponse = requests.get("https://api.guildwars2.com/v2/commerce/prices?ids=%s" % idlist)
        updates = updateresponse.json()
        for itemupdate in updates:
            update = Item.objects.get(item_api_id=itemupdate["id"])
            update.item_sell_price = itemupdate["sells"]["unit_price"]
            update.item_buy_price = itemupdate["buys"]["unit_price"]
            update.save()
        items = Item.objects.filter(selected = True)
    for item in items:
        renderitems.append({'name': item.item_name, 'url': item.item_icon, 'buyprice': item.item_buy_price, 'sellprice': item.item_sell_price})

    context = {'renderlist': renderitems}
    return render(request, 'data/index.html', context)

def chooselist(request):
    try:
        item_list = Item.objects.filter(item_name__icontains=request.GET['searchText'])
    except KeyError:
        item_list = Item.objects.order_by('item_name')
    paginator = Paginator(item_list, 100)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    if len(items) != 0:
        idlist = ""
        for item in items:
            idlist += str(item.item_api_id) + ","
        idlist = idlist[:-1]
        updateresponse = requests.get("https://api.guildwars2.com/v2/commerce/prices?ids=%s" % idlist)
        updates = updateresponse.json()
        for itemupdate in updates:
            update = Item.objects.get(item_api_id=itemupdate["id"])
            update.item_sell_price = itemupdate["sells"]["unit_price"]
            update.item_buy_price = itemupdate["buys"]["unit_price"]
            update.save()

    try:
        item_list = Item.objects.filter(item_name__icontains=request.GET['searchText'])
    except KeyError:
        item_list = Item.objects.order_by('item_name')
    paginator = Paginator(item_list, 100)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {'renderlist': items}
    return render(request, 'data/list.html', context)

def generatelist(request):
    items = get_full_list()
    itemtable = Item.objects.all()
    for item in itemtable:
        item.delete()

    for item in items:
        i = Item(item_api_id=item["id"], item_name=item["name"], item_icon=item["url"], item_buy_price=item["buyprice"], item_sell_price=item["sellprice"], selected=False)
        i.save()
    # items = get_full_list()
    #context = {'renderlist': items}
    # template = loader.get_template('data/list.html')
    return HttpResponse("tada")
    #return render(request, 'data/list.html', context)

def get_full_list():
    rawfile = open('/Users/justinbetz/Documents/testfile.test', 'r')
    rawdata = rawfile.readlines()
    return eval(rawdata[0])

def select_item(request):
    update_item_name = request.GET.get('item_name')
    db_item = Item.objects.filter(item_name = update_item_name)
    if db_item != []:
        item_to_update = db_item[0]
        if item_to_update.selected == False:
            item_to_update.selected = True
        else:
            item_to_update.selected = False
        item_to_update.save()
    return HttpResponse(simplejson.dumps({'success': True}))

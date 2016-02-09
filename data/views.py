from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import simplejson
from .models import Item

# Create your views here.

def index(request):
    items = Item.objects.filter(selected = True)
    print "found " + str(len(items)) + " items"
    renderitems = []
    for item in items:
        renderitems.append({'name': item.item_name, 'url': item.item_icon, 'buyprice': item.item_buy_price, 'sellprice': item.item_sell_price})
    # items = [{'name': u'Superior Rune of the Chronomancer',
    #           'url': u'https://render.guildwars2.com/file/80FE6B56334AB53830DD2D0F61992DF4CC44A710/1201519.png',
    #           'buyprice': '23400',
    #           'sellprice': '29050'}
    #         ,{'name': u'Healing Seeker Coat',
    #           'url': u'https://render.guildwars2.com/file/BBC80CD999BA3994B7C3F9B30F30FE716407E890/61417.png',
    #           'buyprice': '302',
    #           'sellprice': '990'}
    #         ,{'name': u'Precise Seeker Coat',
    #           'url': u'https://render.guildwars2.com/file/BBC80CD999BA3994B7C3F9B30F30FE716407E890/61417.png',
    #           'buyprice': '2054',
    #           'sellprice': '5834'}
    #         ,{'name': u'Precise Seeker Coat',
    #           'url': u'https://render.guildwars2.com/file/BBC80CD999BA3994B7C3F9B30F30FE716407E890/61417.png',
    #           'buyprice': '432',
    #           'sellprice': '3015'}
    #         ,{'name': u'Resilient Seeker Coat',
    #           'url': u'https://render.guildwars2.com/file/BBC80CD999BA3994B7C3F9B30F30FE716407E890/61417.png',
    #           'buyprice': '248',
    #           'sellprice': '1135'}
    #          ]
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
    context = {'renderlist': items}
    return render(request, 'data/list.html', context)

def generatelist(request):
    items = get_full_list()
    itemtable = Item.objects.all()
    for item in itemtable:
        item.delete()

    for item in items:
        i = Item(item_name=item["name"], item_icon=item["url"], item_buy_price=item["buyprice"], item_sell_price=item["sellprice"], selected=False)
        i.save()
    # items = get_full_list()
    context = {'renderlist': items}
    # template = loader.get_template('data/list.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'data/list.html', context)

def get_full_list():
    rawfile = open('/Users/justinbetz/Documents/testfile.test', 'r')
    rawdata = rawfile.readlines()
    return eval(rawdata[0])

def select_item(request):
    print "selecting item"
    update_item_name = request.GET.get('item_name')
    print "updating " + str(update_item_name)
    db_item = Item.objects.filter(item_name = update_item_name)
    if db_item != []:
        print "found item"
        item_to_update = db_item[0]
        if item_to_update.selected == False:
            print "not yet selected"
            item_to_update.selected = True
        else:
            print "already selected"
            item_to_update.selected = False
        item_to_update.save()
    print "done"
    return HttpResponse(simplejson.dumps({'success': True}))

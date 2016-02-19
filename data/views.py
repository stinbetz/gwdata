from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import simplejson
from .models import Item, Recipe, Ingredient
import requests
from django.shortcuts import redirect

# Create your views here.

def index(request):
    items = Item.objects.filter(selected = True)
    renderitems = []
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

def recipes(request):
    renderrecipes = []
    recipes = Recipe.objects.all()

    #update item buy/sell prices
    ingredients = Ingredient.objects.all()
    if len(ingredients) != 0:
        idlist = ""
        for ingredient in ingredients:
            idlist += str(ingredient.item.item_api_id) + ","
        idlist = idlist[:-1]
        updateresponse = requests.get("https://api.guildwars2.com/v2/commerce/prices?ids=%s" % idlist)
        updates = updateresponse.json()
        for itemupdate in updates:
            update = Item.objects.get(item_api_id=itemupdate["id"])
            update.item_sell_price = itemupdate["sells"]["unit_price"]
            update.item_buy_price = itemupdate["buys"]["unit_price"]
            update.save()


    items = Item.objects.filter(selected = True)
    for recipe in recipes:
        cost = 0
        recipe_profit = 0
        renderrecipes.append({"result":{'quantity': recipe.result_quantity, 'item_icon': recipe.result.item_icon, 'item_name': recipe.result.item_name}, 'ingredients': [], 'profit': parse_money_for_display(recipe_profit)})
        ingredients = Ingredient.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            cost += ingredient.quantity * ingredient.item.item_buy_price
            renderrecipes[-1]['ingredients'].append({"item_icon": ingredient.item.item_icon, "item_name": ingredient.item.item_name,"item_buy_price": parse_money_for_display(ingredient.item.item_buy_price),"quantity": ingredient.quantity})
        net = recipe.result.item_sell_price * recipe.result_quantity
        gross = net * 0.85
        recipe_profit = gross - cost
        renderrecipes[-1]['profit'] = parse_money_for_display(recipe_profit)
    context = {'recipelist': renderrecipes, 'itemlist': items}
    return render(request, 'data/recipes.html', context)

@csrf_exempt
@require_http_methods(['POST'])
def create_recipe(request):
    recipe_name = request.POST['recipename']
    ingredients = request.POST['ingredients']
    ingredients = eval(str(ingredients))
    result = request.POST['result']
    result_quantity = request.POST['resultquantity']
    is_mystic_forge = request.POST['isMysticForge']
    if is_mystic_forge == 'false':
        is_mystic_forge = False
    else:
        is_mystic_forge = True

    recipe_result = Item.objects.get(item_name=result)
    newrecipe = Recipe(recipe_name=recipe_name, result=recipe_result, result_quantity=result_quantity, mystic_forge=is_mystic_forge)
    newrecipe.save()
    for ingred in ingredients:
        ingredient_item = Item.objects.get(item_name=ingred['name'])
        new_ingredient = Ingredient(recipe=newrecipe, quantity=ingred['quantity'], item=ingredient_item)
        new_ingredient.save()

    return redirect('recipes')

def parse_money_for_display(value):
    temp = value
    loss = value < 0
    gold, silver, copper = 0, 0, 0
    copper = temp % 100
    if temp >= 100:
        temp = (temp - copper) / 100
        silver = temp % 100
        if temp >= 100:
            temp = (temp - copper) / 100
            gold = temp % 100
    return {'gold': gold, 'silver': silver, 'copper': copper, 'loss': loss}

from .models import *
from django.contrib.auth import logout
from django.db.models import Count
from django.shortcuts import render,redirect,get_object_or_404
from .forms import MomForm,MenuForm,MenuItemForm
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
# Create your views here.
def HomeView(request):
    items = MenuItem.objects.all().select_related('menu')
    context = {"items":items}
    return render(request,'home.html',context)

def ProductView(request,pk):
    item = MenuItem.objects.get(id=pk)
    context = {'item':item}
    return render(request,'product.html',context)

def ProductViewPage(request):
    item = MenuItem.objects.all()
    context = {'items':item}
    return render(request,'productpage.html',context)


def ProfileView(request):
    if request.user.is_authenticated == True:
        user = User.objects.get(id=request.user.id)
        for groupfetch in user.groups.all():
            if (str(groupfetch) == "moms" or str(groupfetch) == "customer" or str(groupfetch) == "delivery"):
                groupname = groupfetch            
        if str(groupname) == "moms":
            email = request.user.email
            print("email" , email)
            mom_obj = MomModel.objects.get(email=email)
            menu_obj = mom_obj.momsmenu.annotate(num_item = Count('menu'))
            context = {"name":"profile","mom":mom_obj,"menus":menu_obj}
            return render(request,"profile.html",context)
        elif str(groupname) == "customer":
            return redirect('customer:customer')
    else:
        return redirect('moms:login')


def ProfileUpdateView(request,pk):
    if request.user.is_authenticated == True:
        mom = MomModel.objects.get(id=pk)
        form = MomForm(instance=mom)
        if request.method == "POST":
            form = MomForm(request.POST,request.FILES,instance=mom)
            if form.is_valid():
                form.save()
                return redirect('moms:profile')
        context = {
            "form":form,
            "formname":"profile update"
        }

        return render(request,"forms.html",context)
    else:
        return redirect('moms:login')

def ProfileDelete(request):
    if request.user.is_authenticated == True:
        mom = User.objects.get(email=request.user.email)
        if request.method == 'POST':
            logout(request)
            mom.delete()
            return redirect('moms:login')
        user = mom.username
        context = {"user":user}
        return render(request,'delete.html',context)
        


def CreateMenu(request):
    user = MomModel.objects.get(email=request.user.email)
    form = MenuForm()
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.moms = user
            try:
                menu.save()
            except Exception as e:
                print("error",e)
            return redirect('moms:profile')

    context = {"form":form,"formname":"createmenu"}

    return render(request,'forms.html',context)

def MenuUpdateView(request,pk):
    if request.user.is_authenticated == True:
        menu = Menu.objects.get(id=pk)
        form = MenuForm(instance=menu)
        if request.method == "POST":
            form = MenuForm(request.POST,request.FILES,instance=menu)
            if form.is_valid():
                form.save()
                return redirect('moms:profile')
        context = {
            "form":form,
            "formname":"menu update"
        }

        return render(request,"forms.html",context)
    else:
        return redirect('moms:login')

def MenuDeleteView(request,pk):
    if request.user.is_authenticated == True:
        menu = Menu.objects.get(id=pk)
        if request.method == 'POST':
            menu.delete()
            return redirect('moms:profile')
        user = menu.name
        context = {"user":user}
        return render(request,'delete.html',context)
    return redirect('moms:login')


def createMenuItem(request):
    if request.user.is_authenticated == True:
        form = MenuItemForm(user = request.user)
        if request.method == 'POST':
            form = MenuItemForm(request.POST or None,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('moms:profile')
            
        context = {'form':form,"formname":"create menu item "}
        return render(request,'forms.html',context)
    return redirect('moms:login')

def MenuItemView(request,mom_id,menu_id):
    if request.user.is_authenticated == True:    
        try:
            mom_obj = MomModel.objects.get(id=mom_id)
            menu_obj = Menu.objects.get(id=menu_id, moms=mom_obj)
            item_obj = menu_obj.menu.all()
            for item in item_obj:
                print("child name",item.name)
        except Exception as e:
            print ("error",e)
        context = {"items":item_obj,"menu":menu_obj}
        return render(request,'items.html',context)
    return redirect("moms:login")


def MenuItemUpdateView(request,pk):
    if request.user.is_authenticated == True:
        item_obj = MenuItem.objects.get(id=pk)
        form = MenuForm(instance=item_obj)
        if request.method == "POST":
            form = MenuForm(request.POST,request.FILES,instance=item_obj)
            if form.is_valid():
                form.save()
                return redirect('moms:profile')
        context = {
            "form":form,
            "formname":"menu item update"
        }

        return render(request,"forms.html",context)
    else:
        return redirect('moms:login')

def MenuItemDeleteView(request,pk):
    if request.user.is_authenticated == True:
        item_obj = MenuItem.objects.get(id=pk)
        if request.method == 'POST':
            item_obj.delete()
            return redirect('moms:profile')
        user = item_obj.name
        context = {"user":user}
        return render(request,'delete.html',context)
    return redirect("moms:login")

def notify_purchase_to_mom(request):
    if request.user.is_authenticated == True:
        user = User.objects.get(id=request.user.id) 
        for groupfetch in user.groups.all():
            if (str(groupfetch) == "moms"): 
                mom = MomModel.objects.get(email=user.email)
                order_query = mom.notify_mom.all()
                for notify in order_query:
                    print("notify id: ",notify.id)

                context = {"order_message":order_query}
                return render(request,"notification.html",context)
            
            return redirect('moms:login')
    
    return redirect('moms:login')

def order_accept(request, pk):
    try:
        notification_obj = get_object_or_404(Notifcation, id=pk)
        order_placed_obj = notification_obj.order_placed
        if order_placed_obj:
            order_placed = OrderPlaced.objects.get(id=order_placed_obj.id)
            order_placed_obj1,created = OrderAccept.objects.get_or_create(order_placed = order_placed,is_ordered = True)
            if created:
                print("notify item object : order accepted ",order_placed_obj1)
            
            print("notify item object : order accepted ",order_placed_obj1)

            return HttpResponse("Order Placed ID: " + str(order_placed_obj.id))
        else:
            raise Http404("OrderPlaced not found for this notification.")
    except Notifcation.DoesNotExist:
        raise Http404("Notification does not exist.")


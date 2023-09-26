from django.shortcuts import render,HttpResponse,redirect
from mom.models import *
from django.contrib.auth.models import User,AnonymousUser
from django.conf import settings
from django.conf.urls.static import static
from customer.forms import CustomerForm

# Create your views here.

def customer_profile (request):
    if request.user.is_authenticated == True:
        user = User.objects.get(id = request.user.id)
        for groupfetch in user.groups.all():
            if (str(groupfetch) == "moms" or str(groupfetch) == "customer" or str(groupfetch) == "delivery"):
                groupname = groupfetch            
        if str(groupname) == "moms":
            return redirect('moms:profile')
        elif str(groupname) == "customer":
            if request.user.is_authenticated == True:
                email = request.user.email
                cust_obj = Customer.objects.get(email=email)
                order = cust_obj.customer.all()
                order_count = order.count()
                context = {'cust_obj': cust_obj,'order_count':order_count,'orders':order}
                return render(request,'customer/customer_profile.html',context)
    
    return redirect("moms:login")

    # if isinstance(request.user,AnonymousUser):
    #     return redirect('moms:home')

def customer_update(request,pk):
    cust_obj = Customer.objects.get(id=pk)
    form = CustomerForm(instance=cust_obj)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=cust_obj)
        if form.is_valid():
            form.save()
            return redirect('customer:customer')
    context = {"form":form,"formname":"update"}
    return render(request,'customer/forms.html',context)

def customer_delete(request,pk):
    cust_obj = Customer.objects.get(id=pk)
    if request.method == 'POST':
        cust_obj.delete()
        return redirect('moms:logout')
    return render(request,'customer/delete.html')


def MomProfileView(request,pk):
    moms = MomModel.objects.get(id=pk) 
    menus = moms.momsmenu.all()
    menu_item = MenuItem.objects.filter(menu__in = menus)  
    print(menu_item)
    context = {'moms':moms,'menus':menus,'menu_item':menu_item}
    return render(request,'customer/mom_profile.html',context)

def MomsProfileView(request):
    moms = MomModel.objects.all()
    context = {"moms":moms}
    return render(request,'customer/mom.html',context) 

def create_or_get_order(request,pk):
    user = User.objects.get(id=request.user.id)
    print("user : ",user)
    group_name = user.groups.all()[0]
    print("outside groupname",group_name)
    if str(group_name) == "customer":
        try:
            customer = Customer.objects.get(user=user)
            item = MenuItem.objects.get(id=pk)
            print("item: ",item)
            order,created = Order.objects.get_or_create(customer=customer,moms=item.menu.moms )
            # order,created = Order.objects.create(customer=customer,moms=item.menu.moms )
            order.items.add(item)
            orderitem,created = OrderItem.objects.get_or_create(order=order,menu_item=item)
            orderitem.status = 'pending'
            orderitem.quantity += 1
            orderitem.save()
            # print("orderitem",orderitem)
            # print("orderitem quantity",orderitem.quantity)
            return redirect ('customer:orderview')
        except Exception as e:
            print("exception ",e)
    
    return HttpResponse("couldnot created")


def OrderView(request):
    item_with_id = request.GET.get('item_id')
    operation = request.GET.get('operation')
    user = User.objects.get(id=request.user.id)
    customers = Customer.objects.get(user=user)
    orders = customers.customer.all()
    context = {'orders':orders}
    if request.method == "GET":
        if item_with_id and operation:
            try:
                item = OrderItem.objects.get(id=item_with_id)
                item.updated_quantity(operation)
            except Exception as e:
                print("error",e)

    # print("item with id " ,item_with_id)
    # print("operation " ,operation)
    # item = OrderItem.objects.get()
    return render(request,'customer/order.html',context)

def order_item_delete(request,pk):
    item = OrderItem.objects.get(id=pk) 
    if request.method == 'POST':
        item.delete()
        return redirect('customer:orderview')
    context = {"item":item}
    return render(request,'customer/delete.html',context)
    
def order_delete(request,pk):
    item = Order.objects.get(id=pk) 
    if request.method == 'POST':
        item.delete()
        return redirect('customer:orderview')
    context = {"item":item}
    return render(request,'customer/delete.html',context)

def buy_order(request,pk):
    ordered_item_obj = OrderItem.objects.get(id=pk) #id=13
    order_placed_obj,created = OrderPlaced.objects.get_or_create(order_placed=ordered_item_obj,is_placed = True)
    print("order id created",created)
    print("buy order")
    context = {'ordered_item':ordered_item_obj,'order_placed':order_placed_obj}
    return render(request,'customer/buy_now.html',context)
    
def notify_purchase_to_customer(request):
    if request.user.is_authenticated == True:
        user = User.objects.get(id=request.user.id) 
        for groupfetch in user.groups.all():
            if (str(groupfetch) == "customer"): 
                customer = Customer.objects.get(email=user.email)
                order_query = customer.notify_order_accept_customer.all() 
                for notify in order_query:
                    print("notify id: ",notify.id)

                context = {"order_message":order_query}
                return render(request,"customer/notification.html",context)
            
            return redirect('moms:login')
    
    return redirect('moms:login')

def accept_order_payment(request,pk):
    order_accept_notification = OrderAcceptNotifcation.objects.get(id=pk)
    order_accept_id = order_accept_notification.order_accept.id
    order_accept_obj = OrderAccept.objects.get(id=order_accept_id)
    total_price = order_accept_obj.order_placed.order_placed.total_price
    quantity = order_accept_obj.order_placed.order_placed.quantity
    
    item_name = order_accept_obj.order_placed.order_placed.menu_item.name
    payment = Payment.objects.get_or_create(payment_method="e-pay", total_amount=total_price,order_accept=order_accept_obj)
    if request.method == "POST":
        recipt = Recipt.objects.get_or_create(payment=payment,recipt_name=item_name)
        return redirect('customer:recipt')
    context = {'payment':payment,'quantity':quantity,'item_name':item_name,'total_price':total_price}
    return render(request, 'customer/payment.html',context)


def recipt(request):

    context = {}
    return render(request,'customer/recipt.html',context)
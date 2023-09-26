from django.dispatch import receiver
from django.db.models.signals import post_save
from customer.models import Customer
from mom.models import *
from django.shortcuts import redirect

# @receiver(post_save,sender=OrderPlaced)
# def create_notify(sender,instance,created,**kwargs):
#     print("===================================")
#     print("instance : ",instance)
#     print("created : ",created)


@receiver(post_save,sender=OrderPlaced)
def create_notif(sender,instance,created,**kwargs):
    cust_grup_name = instance.order_placed.order.customer.user.groups.all().first().name
    cust_id = instance.order_placed.order.customer.id
    mom_id  = instance.order_placed.order.moms.id
    item_id = instance.order_placed.menu_item.id
    order_item_id = instance.order_placed.id
    quantity = instance.order_placed.quantity
    total_price = instance.order_placed.total_price
    mom_obj = MomModel.objects.get(id=mom_id)
    cust_obj = Customer.objects.get(id=cust_id)
    item_obj = MenuItem.objects.get(id=item_id)
    order_item_obj = OrderItem.objects.get(id=order_item_id)

    print("item id ",item_id)
    print("total price",total_price)
    print("order item",order_item_obj)
    if created:
        if str(cust_grup_name) == 'customer': 
            message = f"order from customer = {cust_obj} || order item = {instance.order_placed.menu_item.name} || No of quantity = {quantity} || --- for {mom_obj}  "   
            # message = f"order placed from {cust_obj} for order item {instance.order_placed.menu_item.name} and item id is {instance.order_placed.menu_item.id} --- for {mom_obj} --quantity = {quantity}"
            print("message is" , message)
            create_notify = Notifcation.objects.create(customer=cust_obj,mom=mom_obj,order_placed = instance,message=message)
            # create_order = CopyOrder.objects.create(order_item=item_obj,customer=cust_obj,quantity=quantity,total_price=total_price)
            # order_item_obj.delete()
            # OrderAccept.objects.create(order_accepted = create_notify)
            # instance.delete()
            # return redirect('customer:placed-orders')
            # print("create order ",create_order)
            print("create notification ",create_notify)

    else:
        if str(cust_grup_name) == 'customer':    
            message = f"order from customer = {cust_obj} || order item = {instance.order_placed.menu_item.name} || No of quantity = {quantity} || --- for {mom_obj}  "   
            # message = f"order from customer = {cust_obj} || order item = {instance.order_placed.menu_item.name} || No of quantity = {quantity} || --- for {mom_obj}  "   
            # order_item_obj.delete()
            print("already created notification for that id")
            print(message)        
    
        
    

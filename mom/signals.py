from django.dispatch import receiver
from django.db.models.signals import post_save
from customer.models import Customer
from mom.models import *
from django.shortcuts import redirect


@receiver(post_save, sender=OrderAccept)
def create_notif(sender, instance, created, **kwargs):
    print("instance", instance)
    # print("istance grup name : ", instance.order_accept)
    orderplaced = instance.order_placed.order_placed
    print(orderplaced) 
    cust_grup_name = orderplaced.order.moms.user.groups.all().first().name
    cust_id = orderplaced.order.customer.id
    mom_id = orderplaced.order.moms.id
    item_id = orderplaced.menu_item.id
    order_item_id = orderplaced.id
    quantity = orderplaced.quantity
    total_price = orderplaced.total_price
    mom_obj = MomModel.objects.get(id=mom_id)
    cust_obj = Customer.objects.get(id=cust_id)
    item_obj = MenuItem.objects.get(id=item_id)
    order_item_obj = OrderItem.objects.get(id=order_item_id)

    print("item id ", item_id)
    print("total price", total_price)
    print("order item", order_item_obj)
    print("cust_grup_name", cust_grup_name)
    print("mom_obj", mom_obj)
    print("quantity", quantity)
    print("cust_obj", cust_obj)
    print("item_obj", item_obj)
    create_notify = OrderAcceptNotifcation.objects.create(
                customer=cust_obj, mom=mom_obj,ordered_item=order_item_obj,order_accept=instance)

    if created:
        if str(cust_grup_name) == 'moms':
            if instance.is_ordered==True:
                order_item_obj.status = 'accepted'
                create_notify.message = f"order from mom = {mom_obj} || order item = {orderplaced.menu_item.name} || No of quantity = {quantity} || --- for {cust_obj} is accepted "
                order_item_obj.save()
                create_notify.save()
            else:
                order_item_obj.status = 'canceled'
                create_notify.message = f"order from mom = {mom_obj} || order item = {orderplaced.menu_item.name} || No of quantity = {quantity} || --- for {cust_obj} is cancelled "
                order_item_obj.save()
                create_notify.save()
            print("create notification ", create_notify.message)

    else:
        if str(cust_grup_name) == 'moms':
            # message = f"order from mom = {mom_obj} || order item = {instance.order_accept.menu_item.name} || No of quantity = {quantity} || --- for {cust_obj} is accepted and preparing "
            if instance.is_ordered==True:
                create_notify.message = f"order from mom = {mom_obj} || order item = {orderplaced.menu_item.name} || No of quantity = {quantity} || --- for {cust_obj} is accepted "
                order_item_obj.status = 'accepted'
                order_item_obj.save()
                create_notify.save()
                
            else:
                order_item_obj.status = 'canceled'
                create_notify.message = f"order from mom = {mom_obj} || order item = {orderplaced.menu_item.name} || No of quantity = {quantity} || --- for {cust_obj} is cancelled "
                order_item_obj.save()
                create_notify.save()
            print("already created notification for that id")
            print(create_notify.message)        
    
        
    

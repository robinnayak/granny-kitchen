from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer 

# Create your models here.

class MomModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    kitchen_name = models.CharField(max_length=200,blank=True)
    email =models.EmailField()
    address = models.CharField(max_length=255,blank=True)
    phone_number = models.CharField(max_length=10,blank=True)
    cuisine_type = models.CharField(max_length=200,blank=True) #cuisine_type = itilian food, indian food, 
    profile = models.ImageField(upload_to="mom/profile/",blank=True,null=True)
    banenr = models.ImageField(upload_to="mom/banner/",blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Menu(models.Model):
    moms = models.ForeignKey(MomModel,on_delete=models.CASCADE,related_name='momsmenu')
    name = models.CharField(max_length=200,blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='menu')
    name = models.CharField(max_length=200,blank=True)
    description = models.TextField()
    price = models.IntegerField(default=1)
    item_image = models.ImageField(upload_to="mom/items/",blank=True,null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer')
    moms = models.ForeignKey(MomModel,on_delete=models.CASCADE,related_name='moms')
    items = models.ManyToManyField(MenuItem)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=200,blank=True)
    # status = models.CharField(max_length=20,choices=(
    #     ('pending','pending'),
    #     ('accepted','accepted'),
    #     ('preparing','preparing'),
    #     ('On the Way','On the Way'),
    #     ('delivered','delivered'),
    #     ('canceled','canceled'),
        
    #     ),default='not ordered')
    # is_delivered = models.BooleanField(default=False)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='menu_item')
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.IntegerField(default=0)
    status = models.CharField(max_length=20,choices=(
        ('pending','pending'),
        ('accepted','accepted'),
        ('preparing','preparing'),
        ('On the Way','On the Way'),
        ('delivered','delivered'),
        ('canceled','canceled'),
        
        ),default='not ordered')
    is_delivered = models.BooleanField(default=False)
    
    def updated_quantity(self,operation):
        if str(operation)=="add":
            print("operaton quantity :::: ", self.quantity)
            self.quantity += 1
            total_price = self.menu_item.price * self.quantity 
            self.total_price = total_price
            print("total price in model",self.total_price)
            self.save()
        elif str(operation) =="sub":
            self.quantity -= 1
            total_price = self.menu_item.price * self.quantity
            self.total_price = total_price
            if self.quantity == 0:
                self.quantity = 1
                self.total_price =  self.menu_item.price
            self.save()

            print("sub : updated quantity ",self.total_price)
            return total_price
        

class OrderPlaced(models.Model):
    order_placed = models.OneToOneField(OrderItem,on_delete=models.CASCADE,related_name='order_placed')
    is_placed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


    
class Notifcation(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='notify_cust')
    mom = models.ForeignKey(MomModel,on_delete=models.CASCADE,related_name='notify_mom')
    order_placed = models.OneToOneField(OrderPlaced,on_delete=models.CASCADE,related_name="order_placed_notification")
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class OrderAccept(models.Model):
    order_placed = models.OneToOneField(OrderPlaced, on_delete=models.CASCADE,related_name='order_placed_accept')
    is_ordered = models.BooleanField(default=False) # is_accepted
    
    def __str__(self):
        return str(self.id)
    

class OrderAcceptNotifcation(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='notify_order_accept_customer')
    mom = models.ForeignKey(MomModel,on_delete=models.CASCADE,related_name='notify_order_accept_mom')
    ordered_item = models.OneToOneField(OrderItem,on_delete=models.CASCADE,related_name='order_accept')
    order_accept = models.OneToOneField(OrderAccept,on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class Offer(models.Model):
    moms = models.ForeignKey(MomModel,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
class Review(models.Model):
    moms = models.ForeignKey(MomModel,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    rating = models.IntegerField ()
    comment = models.TextField()

    def __str__(self):
        return self.rating
    
class MomsStar(models.Model):
    moms = models.ForeignKey(MomModel,on_delete=models.CASCADE)
    total_review = models.IntegerField()
    average_rating = models.FloatField()

    def __str__(self):
        return self.total_review

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem,through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.items.name

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)    


class Payment(models.Model):
    payment_method = models.CharField(max_length=200,blank=True)
    total_amount = models.DecimalField(max_digits=8,decimal_places=3)
    order_accept = models.OneToOneField(OrderAccept,on_delete=models.CASCADE,related_name='payment_order_accept')

    def __str__(self):
        return self.total_amount

class Recipt(models.Model):
    payment = models.OneToOneField(Payment,on_delete=models.CASCADE,related_name='payment_recipt')
    recipt_name = models.CharField(max_length=200,blank=True,null=True)
    paid_amount = models.IntegerField(default=0)
    def __str__(self):
        return self.recipt_name
    
class Delivery (models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=200,blank=True)
    delivery_status = models.CharField(max_length=200,default="Pending")
    delivery_person = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.delivery_status
    
    



    



    # def __str__(self):
    #     return self.order_accept.order.moms.user.username
    